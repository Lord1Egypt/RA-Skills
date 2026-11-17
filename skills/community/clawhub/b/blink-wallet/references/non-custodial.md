# Non-Custodial (Spark) Accounts

Use this reference to understand how blink-skills supports **self-custodial
(Spark)** Blink accounts, and how it differs from custodial accounts.

## Source Of Truth

- Blink LNURL server (routes recipients to Blink vs Spark): `blink-lnurl-server`
- Breez Spark SDK (Node build): `@breeztech/breez-sdk-spark` (https://breez.technology)
- Skill scripts: `blink/scripts/_lnurl.js`, `_spark_sdk.js`, `create_invoice_lnaddress.js`,
  `resolve_receiver.js`, `spark_*.js`
- Reference implementation (receive): blink-terminal PR #37

## Two Account Types

|                 | Custodial                       | Non-custodial (Spark)                                       |
| --------------- | ------------------------------- | ----------------------------------------------------------- |
| Keys            | Blink holds them                | User holds a 12/24-word seed                                |
| Auth to skill   | `BLINK_API_KEY`                 | `SPARK_MNEMONIC` (+ `BREEZ_API_KEY`) for signing ops        |
| Balance/history | Blink GraphQL API (`me`)        | Breez Spark SDK (local); **not on the Blink API**           |
| Receive         | `lnInvoiceCreate` mutation      | Public LNURL-pay on `blink.sv` (no creds)                   |
| Send            | `lnInvoicePaymentSend` mutation | SDK `sendPayment` (signs locally); **not on the Blink API** |

Both types share the `blink.sv` Lightning-address domain. The account **type is
not encoded in the domain** — the blink-lnurl-server routes each recipient to
the correct provider internally.

## Receiving (no credentials, no seed)

Any Blink Lightning Address (`user@blink.sv`) can be paid via LNURL-pay, whether
the recipient is custodial or Spark. `create-invoice-lnaddress` does this:

1. `resolve-receiver` probes custodial-first (`accountDefaultWallet`), then falls
   back to `.well-known/lnurlp/{user}`. A hit on the fallback ⇒ non-custodial.
2. It mints a BOLT-11 invoice from the LNURL-pay callback.
3. It detects settlement by polling the **LUD-21 `verify`** URL. For Spark
   recipients this flag is webhook-populated and may lag a few seconds.

### SSRF guard

Two distinct allowlists, because the user-supplied address and the
server-supplied follow-up URLs are different trust surfaces:

| Set            | Governs                                                   | Contents                      |
| -------------- | --------------------------------------------------------- | ----------------------------- |
| Address domain | the user-supplied `user@domain` — the narrow SSRF surface | `blink.sv` only               |
| Service hosts  | server-supplied `callback`, `verify`, redirect targets    | `blink.sv` + `lnurl.blink.sv` |

Blink serves its LNURL callbacks from a dedicated host (`lnurl.blink.sv`),
distinct from the address domain — confirmed against live production metadata.
LNURL is a protocol in which the server hands the client further URLs to fetch,
so the service-host allowlist is enforced at the network boundary — inside the
one function every request funnels through — and re-checked on **every hop**:

| Hop                                      | Checked                                                              |
| ---------------------------------------- | -------------------------------------------------------------------- |
| `.well-known/lnurlp/<user>` metadata URL | host allowlist, HTTPS                                                |
| payRequest `callback`                    | host allowlist, HTTPS                                                |
| LUD-21 `verify`                          | host allowlist, HTTPS                                                |
| every HTTP redirect                      | redirects are followed manually, each `Location` re-validated, max 3 |

Being a local address is **not** a licence to be fetched: only the allowlist
admits a host. Private, loopback and link-local IP literals are refused in every
spelling — `127.0.0.1`, the integer form `2130706433`, `0x7f000001`, `127.1`,
`[::1]`, and IPv4-mapped IPv6 (`::ffff:a9fe:a9fe`, which is what `URL` actually
produces) — including `169.254.0.0/16` cloud metadata. Non-standard ports are
refused unless the caller listed `host:port` explicitly. Plaintext `http` is
permitted only for a local host the caller deliberately allowed; the match is
exact, so `localhost.attacker.example` does not qualify.

**Resolved addresses (v3.0.2):** names are checked too, not only literals. Before
each request attempt (the first URL and every redirect target), a hostname is
resolved and refused if **any** of its addresses is private, loopback,
link-local or metadata, so `ip6-localhost` or attacker DNS such as
`127.0.0.1.nip.io` cannot reach a local service. **Fail closed:** a name whose
address cannot be verified (a DNS error such as `EAI_AGAIN`/`ENOTFOUND`, a
lookup timeout, an empty or malformed answer) is refused, never fetched; a
transient failure is retried like any network fault. The name looked up is
exactly the one the request uses. Loopback names (`localhost`, a trailing-dot `localhost.`,
`*.localhost`, `ip6-localhost`, `ip6-loopback`, `localhost.localdomain`) are
classified as local without DNS. Exempt: hosts you explicitly allowlisted (e.g.
a LAN node by name), and the deliberately permitted regtest `localhost`.

**Known limit:** the fetch resolves the name again, so an answer that was
**verified public** and then changes before the connection (DNS rebinding) is not
caught. Closing that
needs pinning the checked address at the socket layer, which core Node's `fetch`
does not expose without the `undici` package.

### Response binding

A remote server's answer is checked against the request that produced it:

- The callback's `pr` must decode as a BOLT-11 invoice, on the expected network,
  for **exactly** the amount requested. Amountless invoices are refused.
- A LUD-21 `settled: true` is accepted only when its `pr` matches the invoice
  being polled — otherwise another payment's settlement would read as your own.

## Balance / send / history / events (require the seed)

These operations need the account seed and run the Breez Spark SDK headless in
Node (Node 22.4+). Set `SPARK_MNEMONIC` and `BREEZ_API_KEY`.

**Network selection:** all four `spark-*` commands default to Spark **mainnet**.
Override with `SPARK_NETWORK=regtest` or a `--network mainnet|regtest` flag
(flag wins). SDK storage is keyed per network (`~/.blink/spark/<network>-<hash>`),
so mainnet and regtest state never mix. There is no Spark equivalent of Blink's
signet `BLINK_API_URL` staging — production `blink.sv` LNURL receive is the only
receive environment.

**Install requirement:** the SDK persists wallet state through `better-sqlite3`,
a native module compiled at install time (needs `python3`, `make`, a C++
compiler). Under `--ignore-scripts` the package is unpacked but never built and
the SDK suppresses the warning, so `require()` still succeeds. The SDK's own
`defaultStorage()` factory is _lazy_ — it returns an object without opening a
database — so probing it cannot catch this. `connect()` therefore requires
`better-sqlite3` directly and opens an in-memory database, failing with
`SPARK_STORAGE_UNAVAILABLE` and the package-manager-specific build-script
approval step (`npm rebuild better-sqlite3`, `pnpm approve-builds` then
`pnpm rebuild`, `yarn rebuild`). Verify a fix by opening a database, not by
trusting a rebuild exit code — a rebuild can exit 0 without producing a binding.

**Version pinning:** the SDK is pinned to `0.25.0` (v2.6.0; previously
`0.23.1` — `0.24.x` shipped npm-only with no release notes, and the pin
deliberately skipped it). `0.25.0` is a documented GitHub release adding
USDT/USDC receive, Orchestra cross-chain receive, unilateral-exit and
deposit-claim fixes, and a zero-balance stable on-chain send fix. Verified
against the full 748-test suite with zero fallout; the stdout-noise guard and
its pinned-storage regression test carry over unchanged (the duplicate-event
`console.debug` emission is byte-identical in `nodejs/storage`). New SDK
capabilities (USDT/USDC receive, cross-chain) are NOT yet exposed as skill
commands — future surface.

**Invoice validation scope (receive path):** the BOLT-11 check verifies
**structure and request-binding**, not the cryptographic signature. It confirms
the bech32 checksum, network, exact amount, a mandatory payment-hash (`p`) tag,
a mandatory payment-secret (`s`) tag, exactly one description form (`d` or `h`,
not both, not neither), a current non-expired timestamp, a signature whose
recovery id is in `{0,1,2,3}`, and that the description-hash matches
`sha256(LUD-06 metadata)`. It does **not** verify the secp256k1 signature — that
attests the payee node signed the invoice, not that the invoice matches our
request, which is what we are checking. The signature is verified by the paying
wallet before it signs the HTLC, so an unsigned invoice is unpayable (an
availability failure) but cannot redirect funds.

- `spark-balance` → `sdk.getInfo().balanceSats`
- `spark-send` → classify the destination with `sdk.parse()`, then:
  - Lightning Address / LNURL → `sdk.prepareLnurlPay` (fees) then `sdk.lnurlPay` (signs)
  - BOLT-11 invoice / Spark address → `sdk.prepareSendPayment` (fees) then `sdk.sendPayment` (signs)
  - A Lightning Address (e.g. `alice@blink.sv`) is an LNURL-pay destination and
    MUST use the LNURL path — `prepareSendPayment` does not accept it.
  - The classification is an **exhaustive allowlist**: the SDK's `parse()`
    recognizes more types than we pay to (on-chain Bitcoin addresses, BOLT-12
    offers, cross-chain destinations, receive-side methods like
    `sparkInvoice`). Everything outside the four supported types is rejected
    with `UNSUPPORTED_DESTINATION` instead of falling into a payment path it
    was never validated for. Widening the list is a deliberate decision, not
    a default.
- `spark-transactions` → `sdk.listPayments`
- `spark-subscribe` → `sdk.addEventListener`

`spark-send` exits **non-zero** when the SDK reports a `failed` payment status,
so automation cannot read a failed payment as success. `pending` exits zero: it
is still in flight.

**Security:** the seed grants spend authority. It is read only from
`SPARK_MNEMONIC` (never from shell rc files), and never logged or written in
readable form. The SDK's local storage dir is keyed by a non-reversible hash of
the seed.

The BIP39 checksum check **fails closed**. A word count is not validation:
twelve arbitrary dictionary words pass it, and one mistyped word then derives a
_different, valid, empty_ wallet — indistinguishable to the user from losing
their funds. If `bip39` is unavailable the command aborts
(`MNEMONIC_VALIDATOR_UNAVAILABLE`) rather than continuing unverified, because
treating "cannot check" as "checked and fine" silently disables the control.
Neither error echoes the seed.

**Budget controls:** `spark-send` is under the same rolling spend limits as the
custodial pay commands. Configured limits (`BLINK_BUDGET_HOURLY_SATS` /
`BLINK_BUDGET_DAILY_SATS`) are enforced after fee resolution and before
signing — the last possible moment before funds move; an unconfigured budget
does not block an explicit one-shot send; successful/pending sends are recorded
in the spending log; `--force` overrides the check. `spark-fee-probe` and
`--dry-run` move nothing and are never budget-gated.

Two scope notes, both inherited from the shared budget module and identical to
the custodial commands:

- **Principal only.** Budgets count the payment amount, not the routing fee —
  a 100-sat send with a 3-sat fee passes with 100 sats remaining and records 100. The fee is known at check time; counting it would diverge from the
  custodial pay commands' convention.
- **Enforcement is reservation-based.** `reserveBudget` decides AND reserves
  under one lock before the send executes, so concurrent sends can never
  jointly exceed a limit. Success/pending finalizes the reservation; an
  explicit terminal failure releases it. An outcome-unknown error after
  dispatch (timeout, lost response, SDK error) **keeps** the reservation —
  the payment may still settle, so freeing the budget for a retry would
  reopen the race; it is pruned fail-closed after 25h. A failed recording
  after settlement behaves the same way.

## The Breez API key (`BREEZ_API_KEY`)

The Breez Spark SDK will not connect without a Breez API key. This is an
access credential for **Breez's infrastructure** — it is NOT custody: it never
touches the seed, cannot sign, and cannot spend. It is per-_application_, not
per-_wallet_, so any valid key works with any seed.

- In **blink-mobile** the key is baked into the app at build time from CI secrets
  (`app/self-custodial/config.ts` reads `Config.BREEZ_API_KEY`), so users never
  see it. A standalone runner (a VPS agent, this CLI) has no baked-in key and
  must supply its own.
- **Get a free key** at https://breez.technology — via the request form, or
  programmatically (the key is emailed to you):

  ```bash
  curl -d "fullname=<full name>" -d "company=<company>" \
       -d "email=<email>" -d "message=<message>" \
       https://breez.technology/contact/apikey
  ```

Set it as `BREEZ_API_KEY` alongside `SPARK_MNEMONIC`.

## Lightning address (@blink.sv)

The wallet's `user@blink.sv` Lightning address is a **server-side record**
(blink-lnurl-server) keyed to the seed-derived identity pubkey — not wallet
state. blink-skills manages it via the SDK's LN-address lifecycle
(`spark-lnaddress get | check | register | delete`).

**Domain pinning.** The Breez SDK's `defaultConfig('mainnet').lnurlDomain` is
`breez.tips` — Breez's own domain, invisible to blink.sv LNURL routing.
`_spark_sdk.connect()` therefore always sets `lnurlDomain`
(`blink.sv` mainnet / `staging.blink.sv` regtest; `SPARK_LNURL_DOMAIN`
override for other Blink deployments), and `breez.tips` is refused with an
explanatory error. Every LN-address operation and output carries the domain.

**Seed ⇒ address recovery.** On connect the SDK automatically runs
`recover_lightning_address` against the configured domain, keyed by the
identity pubkey and authorized by a signature from the seed. A seed exported
from blink-mobile with a registered address is therefore **discoverable from
the seed alone** — `getLightningAddress()` (and `spark-info`'s
`lightningAddress` field) reports it. This is by design: the address is
public information and the seed holder is its owner.

**Server rules mirrored client-side:** one username per pubkey per domain (a
new registration REPLACES the wallet's previous one); usernames are 3–50
chars `[a-z0-9_]` with ≥1 letter (uppercase is REJECTED client-side — never
silently normalized onto the network), with payment-like prefixes
('1', '3', '\_', 'bc1', 'lnbc1') reserved; phone identifiers are not
supported for Spark; availability is a uniqueness lookup across BOTH account
providers (an available name is claimable by anyone); `anon`-mode accounts
are refused registration and inbound minting.

**On `accountType` (v2.4.0):** spark outputs carry `accountType: 'spark'` —
the wallet kind, full stop. Whether a Lightning address is registered is the
`lightningAddress` / `lnAddressStatus` pair (`spark-info`,
`spark-lnaddress get`): `registered` (recovered from the cache),
`none` (verified negative — the lookup service answered a probe), or
`unverified` (service unreachable; null then means "cannot know", not "no
address"). The probe exists because recovery fails silently inside the SDK —
observed live 2026-09-12: blink.sv management endpoints 404'd while a
registered address existed, and `get` reported a false `registered: false`
(a payment to the address settled fine). The probe proves the service is
REACHABLE — necessary, not sufficient, for the recovery route having run
(they are distinct service operations; the definitive fix is the server-side
pubkey→address lookup requested in blink-lnurl-server#43). `spark-lnaddress get` exits 1 on
`registered: "unknown"` so an unverifiable answer never masquerades as a
verified negative. (`create-invoice-lnaddress` / `resolve-receiver` still
classify a _receiver_ as `type: 'lnaddress'` when Spark-backed — a receiver
classification, unchanged.)

**Out of scope:** transferring an existing custodial blink.sv address to
the Spark wallet (blink-mobile does this via the Galoy
`migrationLnAddressTransfer` mutation with a proof signed by the Spark key —
needs BLINK_API_KEY + seed together; a future command).

## Status & budget policy (cross-path)

The pinned SDK's status union is exactly `completed | pending | failed`. Every
path applies the fail-closed rule to an **outcome-unknown rejection** (the
payment may still settle, so the reservation stays). For an unknown
**status**, only the autonomous l402 path stays reserved — `spark-send`
settles unrecognized statuses (safe under the pinned union) and the custodial
commands release:

| Path                                                                                 | Outcome-unknown rejection            | Explicit terminal failure | Unknown STATUS                                                                                                                                                                         |
| ------------------------------------------------------------------------------------ | ------------------------------------ | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `spark-send` (BTC, token, conversions — all via the shared `dispatchAndSettle` seam) | keep reservation (25h prune)         | release + exit 1          | reads via `isFailedStatus`; anything unrecognized settles/exits 0 (pinned union)                                                                                                       |
| `l402-pay --spark`                                                                   | keep reservation                     | release                   | keep reservation fail-closed (autonomous path); PENDING first polls settlement (`--wait`, default 60s — async settlement is normal for Spark; the preimage/token arrive seconds later) |
| Custodial pay commands                                                               | keep reservation (GraphQL transport) | release                   | PENDING settles; ALREADY_PAID and all other/unrecognized statuses release                                                                                                              |

One shared seam (`dispatchAndSettle` in `spark_send.js`) now carries the
spark-send row — the token/conversion branches previously inlined the policy
and drifted from it (PR #10 review).

## Tokens (USDB / BTKN)

The pinned SDK 0.25.0 supports the full token surface (0.25 adds USDT/USDC
receive on top of the USDB/BTKN surface the skill uses):

- `spark-balance` / `spark-info` surface `tokenBalances` (balances are
  precision-preserving strings; metadata flattened per entry).
- `spark-token-info <usdb|id>` — metadata incl. decimals (`usdb` resolves to
  the Brale mainnet constant; `SPARK_USDB_TOKEN` overrides, required on
  regtest).
- `spark-receive-token <amount>` — mints a Spark invoice for the token
  (decimal units via metadata decimals, or `--base-units`). Spark invoices
  are NOT BOLT-11: they can only be paid by Spark wallets.
- `spark-send --token <id> <amount>` — token sends to Spark addresses/
  invoices; `--from-btc` / `--from-token` attach Flashnet conversions
  (`conversionEstimate` in the prepare output is the quote; `--slippage-bps`
  caps slippage, default 50 bps; failed conversions auto-refund).

  Live-tested (FT3): minimum conversion is **800 sats per `--from-btc` leg**
  (budget ≥1000); round-trip spread ~0.1%; token-only sends to your own
  invoice are refused by the SDK (`Self payment not allowed`) while
  `--from-btc` to the same invoice succeeds — conversions aren't transfers.
  In `spark-transactions`, token rows carry `asset: "token"` +
  `amountBaseUnits`/`amountFormatted` + token metadata; `amountSats` is
  null on token rows (a 999,001-base-unit USDB receive is $0.999, not
  999,001 sats).

- Budget: plain token sends are outside the sats budget (it is a sats
  instrument). `--from-btc` conversions reserve the SATS side of the
  estimate (`amountIn`); `--from-token` spends tokens (no sats reservation).

**Verified live on Spark regtest (2026-09):** `spark-balance` emits
`tokenBalances: {}` for an empty `Map(0)`; `spark-token-info usdb` off
mainnet fails with the `SPARK_USDB_TOKEN` hint; `spark-receive-token
25000000 --base-units --token <id>` mints a real `sparkrt1...` Spark
invoice (fee 0); the SDK **network-checks token identifiers** (a mainnet
`btkn1...` id on regtest is rejected by `getTokensMetadata` and
`fetchConversionLimits` with `Invalid token id` / `Invalid network`), so
regtest conversions need a regtest-native token id. The Lightspark regtest
faucet (app.lightspark.com/regtest-faucet) is browser-only (recaptcha), so
funded token sends/conversions on regtest remain manually verified. A
wallet holding tokens reports per-entry `balance` (string),
`balanceFormatted`, and flattened metadata.

## Scope of this spike

- BTC + BTKN tokens (USDB). No custodial-parity Lightning USD receive
  (LNURL-pay is BTC-only); the token-native path is `spark-receive-token`.
- **Production `blink.sv` only.** Staging (signet vs Spark regtest) is deferred.
- Send is a proof-of-concept demonstrating that agent-side signing works with
  no Blink API change and no server signer/VPS.

## Live-fire checklist (regtest)

Before a release that touches the `spark-*` scripts, run a quick pass against
Spark **regtest** (a regtest seed and a `BREEZ_API_KEY` are required; never
print either):

```bash
export SPARK_MNEMONIC="<regtest seed>"
export BREEZ_API_KEY="<key>"
export SPARK_NETWORK=regtest

blink spark-info                      # getInfo shape matches normalizeInfo expectations
blink spark-balance                   # balance reads, stable=true
blink spark-transactions --limit 5    # listPayments shape matches the normalizer
blink spark-fee-probe <destination> 1 # parse/prepare fee extraction (feeSats non-null)
blink spark-send <destination> 1 --dry-run
```

This is the contract the test stubs emulate; if a real run disagrees with the
stubs, the stubs (not the assertions) are what must change.

**Verified live on Spark regtest (2026-09-11, release 2.2.0 pass):** `spark-info`, `spark-balance`,
`spark-transactions` (including `--offset` and the native `typeFilter`, which
the real SDK accepts), `spark-fee-probe`, `spark-send --dry-run`, and a real
1-sat send settling `completed` with the budget reservation finalizing
correctly. The stub shapes match the real SDK: `getInfo()` returns
`{identityPubkey, balanceSats, tokenBalances}` (the stub is a compatible
subset), `listPayments` normalizes identically, and `parse()`/prepare routing
behaves as mocked.

**Install pitfall seen in practice:** npm silently skips the SDK as an
optional dependency when its own optional native subtree fails to build for
the running Node ABI — on a machine that first installed under Node 20,
`better-sqlite3` was compiled against NODE_MODULE_VERSION 115 and Node 22
needs 127, so every install rolled the SDK back with no error. Recovery:
rebuild the native module against the target Node's headers, e.g.
`npm rebuild better-sqlite3 --nodedir="$(dirname "$(dirname "$(which node)")")"`,
then reinstall.

## API-growth notes (issue #940)

- **Receive needs no Blink API change** — the identifier alone is sufficient.
- Convenience GraphQL mutations could let API devs skip raw LNURL:
  `lnAddressInvoiceCreate` (returns `paymentRequest` + `verify`) and
  `lnAddressInvoiceStatus` (wraps LUD-21 verify). The backend already has the
  unwired `lnurl-server` service hooks (`getIdentifier`, `transferIdentifierToSpark`).
- **Balance and transaction history are the biggest gaps** — they are SDK-local
  and invisible to the Blink API. A read model keyed on the identifier (fed by the
  LNURL server's outbound settlement webhook) would close this.
- **Send is not an API concern** — it must be signed by the seed holder.

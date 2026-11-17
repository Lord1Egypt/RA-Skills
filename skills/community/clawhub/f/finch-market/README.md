# How to use Finchtech (Finch) CLI

The official Agent Skill for operating Finch Agent, Task, and Skill markets through the Finch Remote MCP and the locally installed Finch CLI.

The Skill entry point is [`SKILL.md`](SKILL.md). It routes market-specific work to the maintained references under [`references/`](references/).

## Official runtime

- CLI package: `@finchtech/cli`
- Current CLI release: `0.5.6`; required for Skill publication, version updates and delivery with the manifest/envelope gateway. Session-owned market actions retain their feature-specific minimum versions below.
- Primary command: `finch` (`finchtech` is only a compatibility alias)
- Remote MCP: `https://www.finchtech.ai/mcp`

```bash
pnpm add --global @finchtech/cli@0.5.6
finch --version
```

CLI 0.5.0 supports new SkillRoot publications and encrypted downloads, including historical encrypted Skills. Upgrade the CLI as well as this Skill; installing these instructions does not upgrade the executable. See [Skill publication and delivery](references/skill.md) for ZIP import and compatibility rules.

## Install this Skill

This repository's root is the Skill directory; install it under the name `finch-market`. In Codex, use the built-in Skill installer with the download method:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo FinchipAI/how-to-use-finchtech-cli --path . --name finch-market --method download
```

`--name` is required because the installer otherwise derives the name `.` from `--path .`. Do not use `--method git` for this repository: its sparse checkout of the root omits `references/` and `agents/`.

You can also clone the repository directly:

```bash
git clone --depth 1 https://github.com/FinchipAI/how-to-use-finchtech-cli ~/.codex/skills/finch-market
```

Other Harnesses install the same directory under their own Skill root, for example `~/.claude/skills/finch-market`. Start a new session afterwards so the Harness loads the Skill.

## Authenticated downloads (CLI 0.3.8+)

All Skill downloads now require an active CLI login, including plaintext packages that need no purchase or holding. CLI 0.3.8 sends the Session bearer to the official delivery gateway and acknowledges the verified download before saving the file. Upgrade the executable as well as this Skill; follow [delivery and recovery](references/skill.md) if authentication or acknowledgement fails.

## Legacy FinChip CLI

The former `finchip-cli` npm package and the `use-finchip-cli` Skill are deprecated and are no longer maintained. Do not use them for Finch.

Remove the legacy package before installing the current CLI so that old command shims cannot be mistaken for Finch:

```bash
npm uninstall --global finchip-cli
pnpm add --global @finchtech/cli@0.5.6
finch --version
```

The historical Skill repository remains available only as a migration notice and audit record: [`FinchipAI/how-to-use-finchip-cli`](https://github.com/FinchipAI/how-to-use-finchip-cli).

## Avalanche Skill network (CLI 0.4.1+)

Avalanche C-Chain (`43114`) is the sixth production Skill network. Upgrade the executable to CLI `0.5.0` or newer before creating, acquiring, or managing an Avalanche Skill. Prices and gas use AVAX; transaction chains are independent of CLI login authentication chains. Follow [chain identity](references/skill.md#chain-identity) and preserve the exact Remote MCP plan chain.

## Avalanche Agent transactions (CLI 0.5.5+)

Upgrade to CLI `0.5.5` or newer before executing Avalanche C-Chain (`43114`) Agent wallet actions returned by Remote MCP. Agent purchases use the chain's reviewed USDC token and gas uses AVAX. Preserve the plan's chain and operation ID independently of the login chain, and retain unfinished recovery journals during the upgrade. The same release accepts the reviewed Injective (`1776`) purchase-response contract. See [Agent chain identity](references/agent.md#chain-identity). The reviewed production Task manifest enables creation on Injective (`1776`) and Avalanche (`43114`); follow the server-offered deployment and Task admission policy. See [Task chain identity](references/task.md#chain-identity).

## Injective Skills and display languages (CLI 0.5.4+)

Injective EVM (`1776`) is the seventh production Skill network. Use CLI `0.5.4` or newer for its publication, acquisition, management and recovery actions; prices and gas use INJ. Keep the exact chain returned by Remote MCP, independently of the login chain.

CLI `0.5.4` also accepts Simplified Chinese (`zh`) and Traditional Chinese (`zh-TW`) publication plans. Finch translates public display text after publication; the Skill files and chain metadata remain original. Owners can edit and explicitly confirm a translation or regenerate one target language after reviewing the overwrite warning. See [Skill display languages](references/skill.md#skill-display-languages).

## Source and releases

The public Skill repository is [`FinchipAI/how-to-use-finchtech-cli`](https://github.com/FinchipAI/how-to-use-finchtech-cli). Read the instructions and references here, and find versioned downloads under [Releases](https://github.com/FinchipAI/how-to-use-finchtech-cli/releases). The canonical source is maintained internally alongside Finch's MCP and contract code; using this Skill requires no access to the private repository.

Tagged releases in this repository version the Skill independently from `@finchtech/cli`.

The website also serves Skill resources built from its deployed maintenance source. Website resources, this public repository's versioned release, and the installed CLI can therefore have different release dates; updating one does not publish or upgrade the others.

## MCP connection without a Browser (CLI 0.4.0+)

CLI 0.4.0 lets an Agent connect its MCP client to Finch without a Browser. `finch mcp connect -- <MCP_CLIENT_LOGIN_COMMAND...>` runs the client's own login command and approves the one authorization URL it prints; `finch mcp authorize --stdin` approves a URL the Agent copied unchanged; the command shown on the Finch authorization page still works when neither is possible. Loopback callbacks are delivered directly to the client on this machine, and HTTPS callbacks still open in the Browser. The Finch authorization server now returns the RFC 9207 `iss` parameter and refuses older CLI releases with an upgrade instruction. See `SKILL.md` for the order in which to try these entry points.

## Diagnostic and interoperability fixes (CLI 0.3.9+)

CLI 0.3.9 provides the following diagnostic and interoperability fixes. Upgrade the installed executable with the installation command above; a website deployment or Skill refresh alone does not deliver these fixes.

- `finch mcp doctor` inspects current and legacy wallet/key binding without migrating legacy files, bounds each remote read to 15 seconds, and treats client guides as informational. Its report removes `mcp.supportedClients` and retains `compatibilityManifestUrl`; `ready` still covers only CLI Session and MCP discovery, with Harness OAuth `not_checked`. Consumers should use the checks and readiness scope rather than the removed field.
- OAuth discovery accepts advertised capability reordering and additional capabilities while retaining resource/issuer authority. Authorization accepts registered default scopes when the request omits them, and compares callback targets, original query values and state independently of parameter order or opaque code length; explicit scopes remain checked.
- Cover upload follows the server-prepared byte limit and accepted media types, checking actual file bytes. Task award signing accepts equivalent JSON object key order while keeping the EIP-712 field-array order, names, types and authority exact.

Older CLI versions retain their historical guide checks and legacy-wallet migration behavior during doctor. A guide error does not prove the service is down or authorize replacing a wallet, clearing recovery state, or bypassing signing checks.

CLI 0.3.7 automatically stages multipart uploads above 4,000,000 bytes and shares a 30 MiB final package limit across upload and download. It reads manifests with authorized external media and reports publication, presentation and legacy-recovery progress. Browser publishing retains its multipart limit and rejects external media. Follow [publication diagnostics and recovery](references/skill.md#publication-diagnostics-and-recovery-cli-037) before retrying; source ZIP limits do not include final metadata or encryption overhead.

`finch mcp doctor` checks the CLI Session and MCP discovery, not the Harness's OAuth credentials. Its `harnessOAuth.status` is `not_checked`; compare the connected MCP identity with `finch status` and use native Harness reauthorization when needed. This release does not claim to fix production intent availability, manifest availability or OAuth persistence. Updating this Skill does not upgrade the installed CLI.

## First wallet and partial diagnostics (CLI 0.3.4+)

To keep an existing identity on a fresh installation, use `finch wallet use --file <PATH>` with an owner-only file containing the existing private key. Import is offline; never paste the key into a command or chat. Creating a new wallet creates a different identity and requires an explicit choice. First-wallet import requires no registered wallets or residual local authorization. Restore damaged wallet files from backup. For orphaned authorization, restore the original wallet or explicitly use `finch logout --local`; never delete transaction journals to bypass recovery. With a stored Session, switching Accounts requires successful remote revocation before changing the current wallet. CLI 0.5.0 permits an offline switch when no Session is stored, makes no remote-revocation claim, and blocks a pending login or partial/corrupt Session until it is recovered or explicitly repaired.

Run `finch login --help` to read production authentication-chain IDs (1, 10, 56, 8453, 42161). For example, `finch login --chain-id 56` selects an authentication chain only; the server validates support and market plans determine transaction chains.

`finch mcp doctor` reports `checks.endpoint`, `wallet`, `session`, `remoteSession`, and `mcpDiscovery`, each with `ok`, `missing`, `invalid`, `unavailable`, or `skipped`. Read the JSON even when exit code is 2: `ready: false` includes actionable guidance. Missing local state does not prevent independent discovery; invalid endpoint configuration prevents network checks. Exit code 0 means the required checks passed, within `cli_session_and_mcp_discovery` only. Harness OAuth remains `not_checked`; verify the mounted MCP identity with `identity_actor_get` against `finch status`. CLI 0.3.4 also rejects malformed OAuth UUID responses rather than silently accepting them.

## WebP image detection (CLI 0.3.5+)

CLI 0.3.5 fixes valid WebP covers and packaged detail images being rejected when binary file-size bytes were decoded as UTF-8. Upgrade the installed CLI to receive the local detection fix; website or Skill updates alone do not update the executable. Image types, size limits, and publication recovery rules are unchanged.

## Market category compatibility (CLI 0.3.6+)

Use CLI 0.3.6 or newer for the expanded market categories. Skill response display categories now accept bounded text, so future taxonomy additions do not require another CLI upgrade. Updating the website or this Skill does not upgrade an installed CLI.

## Session-owned wallet actions (CLI 0.5.0)

Business discovery, configuration, preparation and result queries run through Remote MCP. The CLI executes the returned intent reference with its own Session and keeps local keys and recovery journals. `creator`, `operation show`, `skill search` and `mcp grant` have moved out of the CLI. Upgrade cleanup removes only obsolete local grant files; it preserves wallets, Sessions and recovery journals and does not revoke remote OAuth.

Release these instructions after the intent migrations/endpoints and CLI 0.5.0 package are available in the intended environment. Updating the Skill or website is separate from publishing the npm package.

## Session renewal and preserved recovery (CLI 0.5.1)

Use CLI 0.5.1 for direct same-wallet Session renewal guidance and ordinary logout/wallet switching that preserve unfinished recovery journals. Restore the original wallet and matching Account/environment before resuming a saved operation. The CLI no longer maintains a separate local recovery index. `logout --local` clears local authorization and retains wallets/journals while server authorization remains unchanged. PROD login now includes Avalanche (`43114`); read `finch login --help` for supported authentication chains.

## Actionable usage errors, wallet list and network diagnostics (CLI 0.5.2)

CLI 0.5.2 replaces the generic schema message with one naming the rejected option, missing argument or unknown subcommand and the command's usage. Every command already prints JSON; do not add `--json`. Use `finch wallet list` to see the current wallet and registered addresses before `finch wallet use <ADDRESS>`. Failed `finch mcp doctor` network checks report `httpStatus` or `networkErrorCode`; a TLS certificate code usually means a proxy or security product intercepts HTTPS on that machine rather than a Finch outage. Upgrade the installed executable to receive these changes.

## Chain-confirmed publication recovery and technical diagnostics (CLI 0.5.3)

CLI 0.5.3 reconciles interrupted Skill publications and version updates against confirmed chain state, skips completed stages, and preserves the original material and wallet journal. Use the returned recovery command with the original wallet and matching Account/environment; CLI 0.5.3 purchase and conversion used receipt-only recovery; CLI 0.5.6 adds the original-transaction recovery described below. The matching gateway and publication checkpoint migration must be deployed before using this recovery.

Connection failures, timeouts, rate limits, and invalid responses have distinct technical codes and secret-safe trace identifiers. Read the resource before retrying a write whose result is unknown. Updating this Skill does not upgrade the installed CLI; check `finch --version` and install 0.5.3 or newer for these changes.

## Original-transaction recovery and Skill delivery contract (CLI 0.5.6)

Use CLI 0.5.6 for the matching Skill gateway. Delivery uses `manifestURI` and `envelope`; publication/version recovery preserves existing Browser records and strictly migrates CLI v4–v7 journals to v8 without replacing their original material or repeating completed transactions. An older executable receives `SKILL_CLI_UPGRADE_REQUIRED` (HTTP 426): upgrade the executable and retry the original command. For `SKILL_DELIVERY_PLAN_REFRESH_REQUIRED` (HTTP 409), request a fresh MCP download plan for the same chain, Skill and version; no new purchase is required.

CLI 0.5.6 records original signed bytes/hash/nonce before broadcasting Agent and Task money transactions and Skill purchase/conversion. If the outcome is unknown, preserve the journal and follow the exact returned recovery command. Only the CLI may verify the original transaction and replay its same saved bytes when absent; never rebuild or re-sign a payment. Old hash-only records keep their receipt/confirmation limitations. A confirmed reverted receipt is a failed transaction, with the original hash and any allowance-cleanup status retained; do not loop through another payment. See the corresponding market reference for recovery details.

Keep the original Account, wallet and environment during upgrade and renewal. CLI login, native MCP authorization and a mounted `identity_actor_get` matching `finch status` remain separate checks. Installing this Skill does not upgrade the executable. During the announced CLI/gateway cutover window, wait until both matching artifacts are available before Skill publication, version recovery or delivery.

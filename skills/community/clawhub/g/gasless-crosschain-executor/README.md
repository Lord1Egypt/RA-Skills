# Gasless Crosschain Executor

A safety-first workflow skill for building **gasless / intent-based cross-chain swaps** under **local-only** key custody.

This is not a trading strategy. It does not pick when or what to trade. It is the guardrail layer that sits between an AI agent and your wallet, ensuring that anything which gets signed has been:

- normalized into a machine-checkable plan,
- validated against a static rule set,
- bound to a hash you explicitly approved,
- signed by a process the agent itself cannot read keys from.

> **Status:** prototype. Validator + local generator + local signer are tested (52 pytest cases). The Fusion+ HTTP wrappers in `examples/` are illustrative — pin your SDK version and verify endpoints before moving real funds.

---

## Motivation

Cross-chain swaps are irreversible and expensive to mess up. AI agents are convenient at orchestrating them, but they are also susceptible to prompt injection, mis-parameterization, and silent post-validation mutation. Every common "trade through chat" failure mode reduces to one of:

- the agent saw a key that should never have been in chat,
- the agent signed something different from what the user said yes to,
- the agent claimed a route was gasless when it wasn't,
- the agent persisted a refresh token / API key into a saved artifact.

This skill bakes hard refuses for each of those into:

- the agent prompt (`SKILL.md`),
- the JSON validator (`scripts/validate_execution_plan.py`),
- the local key tools (`examples/`),
- the test suite (`tests/`).

---

## Capabilities

| You want to … | Use … |
|---|---|
| Bootstrap a wallet on a fresh machine | `examples/generate_wallet.py {keystore,file,env}` |
| Sign EIP-712 typed data without exposing the key | `examples/local_signer.py` |
| Read balance / allowance / EIP-2612 support | `examples/preflight.py` |
| Quote / submit / monitor 1inch Fusion+ orders | `examples/*_fusion_plus.mjs`, `examples/submit_secret.mjs` |
| Validate a plan and bind it to a user-approved hash | `scripts/validate_execution_plan.py` |
| Run regression tests | `pytest tests/` |
| Embed this as an AI skill | point your agent harness at `SKILL.md` |

Provider status:

| Provider | Type | Pipeline |
|---|---|---|
| **`1inch-fusion-plus`** | cross-chain, gasless | `build_order_fusion_plus → local_signer (typed-data) → submit_fusion_plus → status_fusion_plus → submit_secret`. SDK-backed (`@1inch/cross-chain-sdk`); hash-locked; emits typed-data + submit payload + 0600 secret files in one pass. |
| **`1inch-fusion`** | same-chain, gasless | `build_order_fusion → local_signer (typed-data) → submit_fusion → status_fusion`. SDK-backed (`@1inch/fusion-sdk`); auction-based fill, resolver pays source gas, single signature, no hash-lock. |
| **`1inch-aggregator`** | same-chain, paid | `swap_aggregator → local_signer --mode tx → broadcast_tx`. Returns a regular EVM tx; immediate execution, user pays source gas. |
| `custom` | — | escape hatch; validator accepts the value, no helpers ship. Use only with audited contracts and an explicit threat model. |

Plus three discovery / decision helpers used when expanding open-ended requests like *"buy PEPE"* into a concrete plan: `resolve_token.mjs` (symbol → verified address), `portfolio_scan.py` (multi-chain balance), `preflight.py` (per-chain ERC20 + permit probe). See `SKILL.md`'s "Resolving an open-ended buy request" section for the expansion sequence.

To add a new provider (e.g. LI.FI Intents, deBridge DLN, a custom relayer): (1) write a quote-or-build helper modelled on `examples/build_order_fusion_plus.mjs` (cross-chain) or `examples/swap_aggregator.mjs` (same-chain), (2) extend the validator's `PROVIDERS` set, (3) enumerate the plan-field → typed-data / tx-field mapping in the agent's `local_signer.py` invocation (see `SKILL.md` step 7), and (4) add cases to `tests/`. `references/provider-adapters.md` documents the adapter contract.

---

## Three usage modes

### 1. As an AI agent skill

Point your agent harness at `SKILL.md`. The skill defines a 5-classifier decision tree (design / quote / execute / monitor / bootstrap-wallet) and an 8-step execution workflow that always ends in `local_signer.py`. The agent never sees a key.

The agent will ask for:
- a wallet (or run the bootstrap workflow if there isn't one),
- RPC URLs for source + destination chains,
- a provider API key (e.g. `ONEINCH_DEV_TOKEN`),
- the user's intent (route + amount + recipient).

### 2. As standalone CLI tools

Each script in `examples/` and `scripts/` runs by itself — useful for scripting your own flow or auditing what the agent would do without an LLM in the loop.

```bash
# bootstrap a wallet
python examples/generate_wallet.py keystore

# sign typed-data with strict assertions
cat typed_data.json | python examples/local_signer.py \
    --signer-ref keystore:/Users/me/.config/gxe/wallet.keystore.json \
    --expect-chain-id 137 \
    --expect-verifying-contract 0x111111125421ca6dc452d289314280a0f8842a65 \
    --expect-sender-field maker

# validate a plan and get its canonical hash
python scripts/validate_execution_plan.py plan.json
python scripts/validate_execution_plan.py plan.json --hash-only
```

### 3. As a security-review target

Read in this order:
1. `SKILL.md` — the contract the agent must follow
2. `references/security-policy.md` — explicit do/don't list
3. `references/execution-plan-schema.md` — the canonical plan shape and how the approval hash is bound
4. `scripts/validate_execution_plan.py` — what the validator actually enforces
5. `tests/` — what we tested it against

---

## Install for an AI agent

The skill is markdown + helper scripts. Installing it means dropping the directory into the place your agent looks for skills, then running `./scripts/setup.sh` once to materialize the Python venv and the Fusion+ Node deps.

```bash
git clone https://github.com/galpha-ai/gasless-crosschain-executor.git
cd gasless-crosschain-executor
./scripts/install.sh --target <agent>
```

| Agent / target | What `install.sh` does | Override |
|---|---|---|
| `claude-code` | Copy the tree to `~/.claude/skills/gasless-crosschain-executor/`. Add `--project` to install into `./.claude/skills/` of the current repo instead. | `CLAUDE_SKILLS_DIR=…` |
| `codex` | Copy the tree to `~/.codex/skills/gasless-crosschain-executor/`. | `CODEX_SKILLS_DIR=…` |
| `hermes` | Copy the tree to `~/.hermes/skills/gasless-crosschain-executor/`. | `HERMES_SKILLS_DIR=…` |
| `dir <path>` | Copy the tree to `<path>/gasless-crosschain-executor/`. Use this for any agent whose skills directory we don't have a named target for. | — |
| `chatgpt` | Documentation-only target: prints the steps to paste `SKILL.md` into a Custom GPT. | — |

Useful flags:

- `--link` — symlink the source instead of copying. Edits in this repo show up immediately in the agent. Recommended for development.
- `--no-setup` — skip `./scripts/setup.sh` after install (e.g. when the venv already exists at the target).
- `--force` — overwrite an existing install without asking.

For ClawHub / OpenClaw publishing:

```bash
bash scripts/clawhub-publish.sh
# upload the printed clawhub-upload/ dir at https://clawhub.ai/upload
```

A standalone tarball (for distributing without git) is built with:

```bash
./scripts/build-skill.sh
# produces build/gasless-crosschain-executor.skill (gzipped tar) + build-info.json
```

---

## Quick start

### Prerequisites

- Python **3.10+** (required)
- Node **20+** (optional, only for the Fusion+ helpers in `examples/*.mjs`)

Nothing is installed system-wide; everything lives in `./.venv` and `./examples/node_modules`.

### One-line setup

```bash
./scripts/setup.sh
```

This creates `./.venv`, installs all Python deps from `requirements.txt`, runs `npm install` for the Fusion+ helpers when Node is available, and verifies the install by running the test suite. Re-run any time to upgrade deps in place.

Flags: `--no-tests` (skip verification), `--no-node` (skip npm even if Node is present), `VENV=/some/path ./scripts/setup.sh` (override venv location).

After setup, either activate the venv or run scripts directly:

```bash
# activate, then call scripts as `python ...`
source .venv/bin/activate
python examples/generate_wallet.py keystore

# or call the venv's python explicitly
.venv/bin/python examples/generate_wallet.py keystore
```

### Manual setup

If you want to see exactly what the script does:

```bash
# 1. python deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. (optional) node deps for the Fusion+ helpers
cd examples && npm install && cd ..

# 3. verify
pytest tests/ -q
#   103 passed
node --test tests/*.test.mjs
#   33 passed
python scripts/validate_execution_plan.py references/sample-plan.json
#   plan_hash: 5eedba0e...
#   VALID

# 4. bootstrap a wallet (interactive — runs a backup ceremony on the local TTY)
python examples/generate_wallet.py keystore
```

---

## Things to watch out for

These are the failure modes the skill is *built around* but that no software can fully prevent — they are the operator's responsibility:

- **Never paste a private key into chat.** The skill refuses to accept one. If you want to, stop and run `examples/generate_wallet.py` instead.
- **Always type the approval phrase verbatim.** The agent is not allowed to interpret `yes go ahead` for execution. The exact string is `approve this exact plan: <hash>`, where `<hash>` is what `validate_execution_plan.py --hash-only` prints for *that* plan. The validator re-derives the hash and rejects the plan if even one byte changed.
- **A new wallet needs a recovery test.** Before moving anything beyond test funds, restore the mnemonic on a *different* machine to prove the backup works. The bootstrap script tries to make this hard to skip but cannot enforce it.
- **"Gasless" is route-specific.** `gasless_after_existing_allowance` for token A on chain X does not transfer to token B on chain Y. Re-quote each time.
- **Hash binding is local.** The validator catches mutation between approval and signing on this machine. It does not stop a compromised agent from running an entirely separate transaction with the same wallet — which is why the skill recommends a starter wallet with limited funds for early use.
- **Provider docs change.** SDK versions, endpoints, and supported chains move. The `*.mjs` helpers are illustrative; verify against the current docs before relying on them with real money.
- **Hardware wallet > keystore > file > env.** The `env` and `file` modes exist to unblock first-time users. Migrate to a hardware-backed signer for any wallet you actually fund.

---

## Project layout

```text
.
├── README.md                          ← you are here (human-facing entry point)
├── SKILL.md                           ← contract the AI agent follows
├── references/                        ← reference docs the skill loads on demand
│   ├── execution-plan-schema.md       ← plan JSON shape + canonical-hash rules
│   ├── provider-adapters.md           ← 1inch Fusion+ / Aggregator notes + new-provider integration template
│   ├── sample-plan.json               ← validator-accepted minimal plan
│   └── security-policy.md             ← key handling, approvals, allowed artifacts
├── scripts/
│   └── validate_execution_plan.py     ← the gatekeeper (canonical hash + binding)
├── examples/                          ← runnable local tools
│   ├── README.md
│   ├── generate_wallet.py             ← keystore / file / env bootstrap with backup ceremony
│   ├── local_signer.py                ← EIP-712 signer with independent assertions
│   ├── preflight.py                   ← balance / allowance / EIP-2612 reader
│   ├── quote_fusion_plus.mjs
│   ├── submit_fusion_plus.mjs
│   ├── status_fusion_plus.mjs
│   ├── submit_secret.mjs
│   ├── sample_typed_data.json
│   ├── requirements.txt               ← Python deps (eth-account, web3)
│   └── package.json                   ← Node deps (@1inch/cross-chain-sdk)
└── tests/
    ├── README.md
    ├── conftest.py
    ├── test_validator.py              ← 49 boundary cases + 1 sample-hash regression
    ├── test_canonical.py               ← 7 cases for canonical-hash + post-approval binding
    ├── test_local_signer.py            ← 17 cases for typed-data assertions + signer_ref schemes
    ├── test_tx_signer.py               ← 11 cases for --mode tx (chainId/to/value/data binding, EIP-1559)
    ├── test_generate_wallet.py         ← 8 cases for mnemonic/key derivation + file perms
    ├── test_preflight.py               ← 5 cases for ERC20 + permit probe (web3 mocked)
    ├── test_portfolio_scan.py          ← 6 cases for multi-chain balance scan + metadata enrichment
    ├── fusion_plus.test.mjs            ← 8 cases for Fusion+ HTTP helpers (localhost stub)
    ├── build_order.test.mjs            ← 6 cases for Fusion+ SDK order construction
    ├── build_order_fusion.test.mjs     ← 7 cases for Fusion (intra-chain) SDK order + submit + status
    ├── swap_aggregator.test.mjs        ← 3 cases for /swap endpoint shape + slippage math
    ├── resolve_token.test.mjs          ← 5 cases for symbol/address resolution + impostor warnings
    └── broadcast_tx.test.mjs           ← 4 cases for eth_sendRawTransaction wrapper
    └── test_canonical.py              ← canonical hash + post-approval binding gate
```

---

## What the validator actually enforces

A plan is `VALID` only if all of the following hold (full list in `scripts/validate_execution_plan.py`):

- `schema_version` is `"1.0"`.
- `mode`, `provider`, `gasless_verdict` are in their respective enums.
- `wallet.address` is a valid EVM address when `chain_type == "evm"`.
- `wallet.signer_ref` uses one of `env: / file: / keystore: / hw: / signer:` and is *not* a literal key.
- `route.amount_in` and `min_amount_out` are positive decimal strings in smallest units.
- `route.slippage_bps` ∈ [0, 500] (warns above 300).
- `route.deadline_unix` is a future timestamp in execute mode.
- `contracts` includes the spender / settler / verifying contract.
- A `fully_gasless` / `gasless_after_*` verdict cannot coexist with a positive `source_native_gas_required` or a required approval.
- An insufficient `current_allowance` is not silently allowed; either `required: true` or a gasless permit path must be declared.
- `safety.require_explicit_user_approval` is `true`.
- `safety.max_loss_bps` ∈ [0, 500].
- `safety.allowed_terminal_states`, when present, is a non-empty list of strings.
- No sensitive key names appear anywhere in the plan: `private*`, `mnemonic`, `seed_phrase`, `keystore_password`, `password`, `raw_secret`, `api_key`, `bearer*`, `(access|refresh|auth)_token`, `client_secret`, `^secret$`. (`secret_hash` and `secret_hashes` are explicitly whitelisted because they store hashes, not secrets.)
- In `execute_after_user_approval` mode, `safety.user_approved_plan_hash` exists and equals the canonical hash of the plan with that field zeroed out — the binding gate that prevents post-approval mutation.

---

## Testing

```bash
# Python: 103 cases across 7 files
pytest tests/ -v

# Node: 33 cases across 6 files (Fusion+ / Fusion / Aggregator / token resolver / broadcast)
node --test tests/*.test.mjs
```

The full suite (136 cases) runs from `./scripts/setup.sh` after install. Adding a new validator boundary check is a single tuple in `tests/test_validator.py::CASES`. The sample plan's canonical hash is asserted by `test_sample_plan_hash_unchanged`, so external references to it cannot break silently. The Node suites stub the 1inch HTTP API with localhost servers and a fixture quote response — no real keys, tokens, or RPC calls are needed.

---

## License

[MIT](./LICENSE) © 2026 GAlpha.

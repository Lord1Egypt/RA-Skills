---
name: apow-mining
description: Set up APoW Easy Mode on a supported assistant runtime, verify secure wallet recovery before funding, and use x402 remote GPU grinding.
allowed-tools: Bash(npx --yes apow-cli@0.12.3 --version) Bash(npx --yes apow-cli@0.12.3 start --easy) Bash(npx --yes apow-cli@0.12.3 wallet verify-recovery)
metadata:
  openclaw:
    requires:
      anyBins:
        - npx
---

# APoW Mining

Use the official CLI to mine AGENT on Base with a dedicated, recoverable wallet.
Keep only the approved working ETH and USDC balance. Mined AGENT cannot transfer
until the protocol's LP deploys, so this wallet is a long-lived vault: rewards
cannot be swept to make an expendable wallet safe.

## Runtime choice

Read the [personal assistant profiles](https://apow.io/docs/technical/assistants)
for Grok Bot, Muse, Instinct, Wajo/Fo, ChatGPT dots, Claude Duet, OpenClaw, Hermes, Claude Code, Codex,
Manus, Cowork, and Perplexity. Check Node 20+, outbound HTTPS, persistent files,
secure CLI unlock, and the permitted process lifetime before funding.

Use **Easy Mode**: wallet-paid RPC, mint LLM, and x402 remote GPU grinding.
A runner is still required to sign and submit transactions. Do not rent a VPS
or switch to CPU mining by default. The current web app also needs its browser
tab open; fully managed APoW jobs are [under development](https://apow.io/docs/technical/managed-mining).
Do not claim that they are already available.

## Choose a signing runtime before funding

Remote grinding supplies the GPU work. The CLI runner still needs to sign x402
payments and Base transactions. A saved browser login is not a wallet signer.
Do not read browser cookies, extract protected credentials, or weaken a platform
restriction to make mining work. Follow the assistant's and host's rules for
mining, signing, payments, and unattended execution.

Do not create, import, or unlock a mining wallet on an assistant's own cloud
computer or disposable task VM. A remembered conversation or persistent directory
does not prove independent recovery after account loss or a platform reset.

[APoW Cloud Mining](https://apow.io/docs/technical/managed-mining) is the intended
default for assistants, **but is not released**. Stop before wallet creation or
funding on that path. Do not invent a connector, endpoint, or signup flow.

Direct Easy Mode remains an opt-in path on the user's own trusted computer through
a supported execution tool. Require Node 20+, permitted execution, host-local
secure unlock, a proven off-device restore, and a reliable stop. The user must
choose this mode and keep the host available. An assistant that can execute code
beside an unlocked signer has signing authority; a keychain does not eliminate it.

### Grok Bot

Wait for Cloud Mining by default. A previous successful CLI run on a bot's cloud
computer is not evidence of recoverable custody. Do not put a wallet there.
If the user chooses their own connected computer, first prove that commands run
on that host. Test version, recovery, and stop/restart there before requesting funds.
Keep one wallet and one runner; never launch another miner from a status routine.

### ChatGPT dots

Distinguish the dot's cloud computer, a delegated cloud task, and the user's
connected computer. Only the last is a candidate for direct Easy Mode here.
Prove the selected host and its supported local signer; never substitute a network
credential placeholder for a keystore password. Verify how to stop the actual
miner: ending a conversation or delegated task is not proof that mining stopped.

### Muse

Use Cloud Mining once released. Do not create or unlock a wallet in the Secure VM.
A browser vault or connector credential is not evidence of a CLI signing path.
Future integration should use scoped APoW job access, with user authorization
outside chat. No Muse connector or funded mining pass is available from this skill.

### Instinct

Use the user-facing Cloud Mining flow once released. Do not assume terminal,
daemon, or custom-connector support. Until a supported integration is tested,
hand off to the user and stop before wallet creation or funding.

### Wajo / Fo

Use Cloud Mining once released, independently of whether the assistant remembers
earlier chats. Chat memory is not wallet recovery. Never give a wallet secret to
the assistant or human support. If only links are supported, the user operates
APoW; do not claim Fo can start jobs. A new chat must reuse the existing account.

### Claude Duet

Wait for Cloud Mining. Browser credentials and connector access do not establish
a local wallet signer. A future supported connector gets job controls only, with
the platform's approval rules preserved. Do not assume a local-computer bridge
exists or ask the user to place wallet secrets in the assistant's environment.

No complete per-agent end-to-end pass is recorded for these six assistants.
Record the actual host, public wallet address, non-secret unlock method, independent
restore result, runner lifetime, and stop result. Other local CLI agents must meet
the same requirements; an unsupported runtime waits for Cloud Mining.

Cloud Mining is intended to keep the user-owned wallet and mining job independent
of the assistant's chat. After a reset, reconnect through supported account
authentication to the same wallet and job; never create replacements. The
assistant must not receive the wallet key or recovery secret. These are release
requirements, not existing capabilities. Platform restrictions still apply.

## Scope and approval

Before running `start --easy`, check for an unresolved grind-service payment or
response incident. If one exists, stop at version and recovery checks. A funded
wallet can make `start --easy` spend immediately.

Explain once: one dedicated encrypted wallet, one rig mint within the local
policy, ETH-to-USDC funding conversion, x402 services, and continuous Base
mining transactions until stopped. Give the applicable caps and real costs.
Obtain explicit approval if this scope has not already been approved. Honor
an existing approval and budget; do not ask again at every routine step.
Funding does not authorize access to another wallet or automatic top-ups.
Do not enable AGENT sweeps while transfers are locked. After unlock, any transfer
still requires the user's approval; sweeping is never a substitute for recovery.

```bash
npx --yes apow-cli@0.12.3 start --easy
```

For a capability check without wallet activity, run `npx --yes apow-cli@0.12.3 --version`.
Use this pinned Easy Mode flow and the recovery check below for mining.
If the package is unavailable, report it; do not substitute `latest`.

## Recover before funding

The user enters a password directly in a trusted terminal, or uses a supported
secret manager. Never ask for a password, private key, or recovery phrase in chat.
For headless operation, a secret-manager `KEYSTORE_PASSWORD_CMD` reference must
be saved in the private runner configuration. A password generated only in
process memory is not recoverable after a restart. A browser credential vault
must not be assumed to provide CLI secrets.
Let the CLI consume the secret-manager output internally. Never print it to
verify the command or put its value in the agent's context.

```bash
npx --yes apow-cli@0.12.3 wallet verify-recovery
```

CLI 0.12.3 checks a fresh-process unlock of the **same address**. It does not
enforce off-device backup: `wallet verify-backup` is not implemented in this
version. Never report `verify-recovery` as proof that a lost host can be recovered.

Before requesting funding, the user must restore their encrypted backup on a
separate trusted device using independently recoverable unlock material and
verify the same public address. Keep backup and unlock material separate; do not
copy either into chat, an assistant VM, or this repository. A same-host temporary
directory or an unconfirmed cloud-sync folder is insufficient. Record only the
address and successful restore outcome. If this cannot be proven, stop before
funding or mining. Keep an existing locked wallet; do not replace it.

## One deposit

Ask for **Base ETH only**, using the complete address and live amount printed
by the CLI. The quote includes the current rig fee, conservative ETH reserve,
swap gas, and a missing 2 USDC service budget. It is not a fixed USD quote.
Do not ask the user to buy or send USDC separately. After deposit, rerun the
same pinned start command: it converts the required ETH, checks landed balances,
and mints or resumes an existing rig. It stops before a swap that would consume
the ETH reserve.

Solana SOL/USDC funding exists only with a configured Squid integration and a
verified deposit-address quote. Never send SOL to the Base EOA. That optional
bridge route requires the separate funding guide and the user's choice of asset;
this default skill uses the Base ETH handoff.

## Run and report

For a first compatibility test, obtain a finite run duration and spending budget
before the funded run. Start with the capability and recovery checks only.
Verify how the exact runner will stop before starting it. If no reliable stop
mechanism exists, do not begin a finite paid test. A stated budget or timer is
not proof of an enforced spending limit.
Use the same wallet throughout the test. Do not start a paid test when the grind
service has an unresolved payment or response failure.

Start one runner per wallet. Record its process handle and inspect recent logs.
Use the assistant profile's supported background mechanism. A background PID
is not proof of survival after a session or VM ends.

Report these states accurately: wallet recovery verified; awaiting ETH; funded;
rig minted or found; runner active; first confirmed mine. Show a Base transaction
hash for a confirmed mine. A health check or remote GPU request alone is not a
mine. Never invent network activity, competing GPU counts, yield, or profitability.

A passed end-to-end test requires a valid returned remote nonce, its reconciled
x402 payment, a confirmed Base mining transaction, and a clean stop with no
duplicate runner. A later restart must recover the same wallet. Record which
steps passed and the exact failure at any remaining step; setup alone is not a pass.

Do not use local CPU or GPU mining in this skill, including after a remote error.
Local mining is a separate, explicitly requested experiment. A quiet-network
success does not establish useful performance under competition.

## Policy and failure handling

Keep the default signing policy in enforce mode. Default ceilings are 0.01 ETH
per rig mint, 1 USDC per x402 request, and 20 USDC per UTC day. Swaps have their
own 0.02 ETH ceiling. Lower user-approved limits take precedence. These ceilings
do not constitute a hard USD cap on gas, swaps, hosting, or exchange-rate changes.
Never raise caps or disable enforcement to make a task proceed.

- Locked wallet or missing durable secret: repair supported local unlock; no replacement wallet.
- Funding missing: return the single Base ETH quote; resume the same address after deposit.
- Unsupported runner: report the missing capability and route to Cloud Mining when released; until then, stop before wallet creation or funding.
- Policy denial: stop and report the requested action and cap.
- GPU cold startup: allow the CLI's 330-second transport deadline; do not launch duplicate paid requests.
- Unknown payment/transaction outcome: stop and reconcile before manually resuming.
- Normal transient failures: let the CLI's bounded retries run; do not silently change mode.
- User stop: stop the process and report any in-flight transaction or unresolved payment.

Keep wallet secrets out of logs, project files, repositories, agent memory, and
other agents' workspaces. Do not search for credentials or operate a main wallet.

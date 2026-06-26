# Claw Wallet Skill

Local sandbox wallet skill for OpenClaw and Claude Code agents. Install the sandbox locally, operate through localhost APIs or CLI, and support both local wallets and phase2 remote-managed wallets.

## Claude Code marketplace

This repository is now structured so it can be added as a third-party Claude Code marketplace.

Use:

```bash
/plugin marketplace add <this-repo-url>
/plugin install claw-wallet@claw-wallet-marketplace
```

This is a community marketplace setup, not an Anthropic-curated listing. To appear in Anthropic's official directory, the repo still needs to pass their review and submission flow.

## Installation

Skill assets are hosted at **`https://www.clawwallet.cc`**. Deploy that site so these paths exist: **`/install`** (same body as `install.sh`), **`/install.ps1`**, **`/SKILL.md`**, **`/claw-wallet.sh`**, **`/claw-wallet`**, **`/claw-wallet.ps1`**, **`/claw-wallet.cmd`**, and **`/bin/<platform binary>`**.

### Linux / macOS (recommended)

From the workspace root:

```bash
mkdir -p skills/claw-wallet
cd skills/claw-wallet
curl -fsSL https://www.clawwallet.cc/install | bash
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Path "skills\claw-wallet" -Force | Out-Null
Set-Location "skills\claw-wallet"
Invoke-WebRequest -Uri "https://www.clawwallet.cc/install.ps1" -OutFile "install.ps1" -UseBasicParsing
& ".\install.ps1"
```

### Option: npx skills add

For the `dev` test environment, prefer Option 1 so the local checkout is pinned to the `dev` branch explicitly.

```bash
npx skills add ClawWallet/Claw-Wallet-Skill -a openclaw --yes
```

Then run the installer from the cloned skill directory (or use the curl flow above instead of git).

### Developing from this repo

Run `bash install.sh` or `install.ps1` inside `skills/claw-wallet` with **`CLAW_WALLET_SKIP_SKILL_DOWNLOAD=1`** to keep local `SKILL.md` and wrappers without overwriting them from the CDN.

## After install

Verify status:

- `GET {CLAY_SANDBOX_URL}/health` — expected: `{"status": "ok"}`
- `GET {CLAY_SANDBOX_URL}/api/v1/wallet/status` with `Authorization: Bearer <token>` — confirm wallet is ready

Token and URL are in `skills/claw-wallet/.env.clay`.

## Documentation

See [SKILL.md](./SKILL.md) for full documentation, API reference, and agent rules.

# Auto Authenticator Local

Auto Authenticator Local is an OpenClaw skill and local toolset for generating TOTP codes from secrets stored in the operating system's secure credential store.

It is built for legitimate account owners and authorized operators who want:

- local-only secret storage
- no cloud sync requirement
- explicit, on-demand 6-digit TOTP generation
- a simple OpenClaw-compatible skill folder they can install or publish

## Why this exists

Many people already use TOTP-based login prompts during approved automation or repetitive admin work. This project makes that workflow local, small, and auditable:

- TOTP seeds are stored in the system credential vault
- codes are generated only when explicitly requested
- the implementation is pure Python with OS-native secure storage via `keyring`
- no secrets are written to git or plaintext config files

## Safety boundary

This project is not for bypassing MFA policy, evading anti-abuse systems, or hiding OTP generation from security controls. It is meant for accounts the user personally owns or is explicitly authorized to manage.

## Features

- Store a TOTP seed under a short alias
- Generate a 6-digit code with remaining lifetime
- Delete aliases cleanly during rotation or offboarding
- Use the same folder as an OpenClaw skill
- Publishable to ClawHub as a transparent, local-first utility
- Cross-platform secure storage through the operating system key store

## Why people will like it

- It is local-first: secrets stay in the system key store instead of random config files.
- It is small: pure Python with one standard cross-platform dependency.
- It is explicit: no hidden background generation, no mystery side effects.
- It is practical: easy to wire into approved repetitive login workflows.
- It is auditable: the storage and generation path is short and readable.

## Requirements

- macOS, Windows, or Linux
- Python 3.11+
- `pip install -r requirements.txt`
- OpenClaw only if you want the skill behavior inside OpenClaw

## Quick start

One-line install:

```bash
curl -fsSL https://raw.githubusercontent.com/LucasZH7/auto-authenticator-local/main/install.sh | bash
```

This installer clones the repository into `~/.openclaw/skills/auto-authenticator-local` by default and installs Python dependencies locally for the tool.

Install dependency:

```bash
python3 -m pip install -r requirements.txt
```

Store a seed:

```bash
python3 scripts/totp_add.py --alias github-work --issuer GitHub --account lucas@example.com --seed JBSWY3DPEHPK3PXP
```

Generate a code:

```bash
python3 scripts/totp_code.py --alias github-work
```

Delete an alias:

```bash
python3 scripts/totp_delete.py --alias github-work
```

## OpenClaw usage

Place this folder inside your workspace skills directory or install it through ClawHub later. The skill instructs the agent to use the bundled scripts explicitly and safely.

## Secure storage backends

- macOS: Keychain
- Windows: the backend exposed through `keyring`, typically Credential Manager
- Linux: the backend exposed through `keyring`, typically Secret Service or KWallet

On macOS, the scripts also keep a native fallback through the built-in `security` CLI if `keyring` is unavailable.

## Development

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Publish notes

- GitHub repo: ready to publish as an open repository
- ClawHub: publish as a public skill with privacy-first tags and a compliant description
- Positioning: local TOTP helper, privacy-first, transparent, explicit, auditable

## Suggested listing copy

Short pitch:

> A local-first TOTP helper for OpenClaw users who want private, explicit, on-device code generation with macOS Keychain storage.
> A local-first TOTP helper for OpenClaw users who want private, explicit, on-device code generation with system-vault-backed storage.

Highlights:

- Local-only secret handling
- System-vault-backed storage
- Fast 6-digit generation
- Small and readable implementation
- Built for legitimate, authorized access workflows

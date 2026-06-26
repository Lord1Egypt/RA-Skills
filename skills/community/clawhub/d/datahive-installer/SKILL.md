---
name: datahive-installer
description: "Automates DataHive sign-in using a magic link workflow: requests the link, retrieves it from Gmail via gog, and opens it in a Chrome DevTools tab."
metadata:
  openclaw:
    emoji: "🍯"
    requires:
      bins: ["gog", "curl", "websocat"]
---

# datahive-installer

Automates installation of DataHive node.

## DataHive context (for operators)

DataHive is a platform for high-quality AI training datasets and analytics use cases across domains such as e-commerce, reviews, audio, image, and video, with an emphasis on decentralized and passive data collection workflows. This skill is limited to dashboard authentication automation, specifically requesting a magic link, retrieving it, and opening the login tab, and does not cover dataset management.

## Trigger phrases

Use this skill when the user says things like:

- "run datahive-installer"
- "log me into DataHive"
- "start DataHive login flow"
- "execute DataHive installer"
- "setup DataHive"
- "install DataHive"

## Execution rule

Always execute this skill in the exact sequence defined in **strict order**, exactly as written in this `SKILL.md`.
Do not skip, reorder, or parallelize steps unless the user explicitly asks to change the sequence.

## What this skill does

0. Detect platform (ubuntu or macos) and stop with an error for any other OS.
1. Install runtime prerequisites for the detected platform.
2. Launch Chrome in persistent background mode with CDP enabled.
3. Read your authenticated gog account email.
4. Request a DataHive magic link via API.
5. Find the latest DataHive login email in Gmail.
6. Extract the magic login URL.
7. Open the magic URL in a new browser tab over CDP.

## Step 0 — Detect platform

Run:

```bash
./scripts/0_detect_platform.sh
```

Expected output:
- `ubuntu` for Ubuntu hosts
- `macos` for macOS hosts

Any other value or non-zero exit means unsupported platform.

## Step 1 — Install prerequisites (platform-aware)

Run:

```bash
PLATFORM="$(./scripts/0_detect_platform.sh)" ./scripts/1_install_prerequisites.sh
```

Behavior by platform:
- `ubuntu`: installs Chrome + xvfb via `apt`, applies managed extension policy, installs `websocat`.
- `macos`: installs Chrome via Homebrew cask (if missing), applies managed extension policy in `/Library/Managed Preferences/com.google.Chrome.plist`, installs `websocat`.

## Step 2 — Launch browser in persistent background mode (platform-aware)

Run:

```bash
PLATFORM="$(./scripts/0_detect_platform.sh)" ./scripts/2_launch_chrome_supervisor.sh
```

Behavior by platform:
- `ubuntu`: launches `google-chrome` under `xvfb-run`.
- `macos`: launches `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` directly.

Optional checks:

```bash
curl -sf http://localhost:9222/json/version
```

```bash
tail -f "$HOME/.chrome-datahive/chrome.log"
```

## Step 3 — Get email from gog

```bash
gog auth list --json
```

Use the default account email from output (example: `peter@gmail.com`).

## Step 4 — Request magic link

Use the helper script with your gog email:

```bash
./scripts/4_request_magic_link.sh <EMAIL>
```

(or `EMAIL=<EMAIL> ./scripts/4_request_magic_link.sh`)

Expected response:

```json
{"message":"If this email exists, a login link has been sent"}
```

## Step 5 — Find latest DataHive magic-link email

```bash
gog gmail messages search 'from:datahive newer_than:7d' --max 10 --account <EMAIL>
```

Take the top/latest message ID and fetch it:

```bash
gog gmail get <MESSAGE_ID> --account <EMAIL> --json
```

Extract the URL from the HTML body:

`https://dashboard.datahive.ai/auth?token=...`

## Step 6 — Open magic link

Run:

```bash
TARGET_URL='https://dashboard.datahive.ai/auth?token=<TOKEN>' ./scripts/6_open_magic_link.sh
```

## Notes

- Magic links expire quickly (about 15 minutes).
- Treat magic links as secrets; do not share them.
- If CDP is not available, start Chrome with remote debugging enabled.

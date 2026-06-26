---
name: freeguard-setup
description: Guide users through installing, signing in to, connecting, and troubleshooting FreeGuard VPN with the official FreeGuard CLI.
version: 0.8.9
metadata:
  openclaw:
    requires:
      bins:
        - freeguard
    install:
      - kind: brew
        formula: planetlinkinc/tap/freeguardvpn
        bins:
          - freeguard
    homepage: https://freeguardvpn.com
---

# FreeGuard VPN Setup Guide

Use this skill when a user wants help setting up, using, or troubleshooting FreeGuard VPN through the official `freeguard` CLI.

Keep the user-facing tone friendly and plain. Explain what is happening, ask for confirmation before account or payment actions, and avoid exposing internal configuration names unless the user asks for technical detail.

## Security Boundaries

This skill is an instruction-only guide. It does not include scripts, binaries, background services, account credentials, or network clients. All VPN, account, subscription, and local configuration operations are performed by the `freeguard` CLI on the user's computer.

Respect these boundaries:

- Do not ask the user to paste long-lived credentials or subscription tokens into chat.
- Do not handle passwords, payment card details, or verification codes outside the CLI or browser flow.
- Do not run account, billing, or connection-changing commands without telling the user what will happen.
- Prefer the standard non-elevated connection flow. Only discuss system-wide protection when the user explicitly asks for it.
- If provenance or review evidence is needed, read `references/provenance.md`.

## Install Or Verify The CLI

First check whether the CLI is already available:

```bash
freeguard version
```

If the command is present, continue to setup. If it is missing, recommend the official Homebrew formula on macOS or Linux:

```bash
brew install planetlinkinc/tap/freeguardvpn
```

After installation, verify again:

```bash
freeguard doctor --json
```

For Windows, or for macOS/Linux users who cannot use Homebrew, guide the user to download the latest platform asset from the official GitHub Releases page in their browser, verify the published SHA256 checksum, extract the binary, and place it in a user-writable directory already on PATH. Do not automate this fallback unless the user asks for step-by-step terminal help.

## Setup Flow

Run diagnostics and summarize the result:

```bash
freeguard doctor --json
```

Use the result to choose the next step:

- CLI missing: go to "Install Or Verify The CLI".
- Not signed in: go to "Sign In".
- No active subscription: go to "Subscription".
- Ready: go to "Connect".

Use friendly summaries:

- "FreeGuard is installed. Now let's sign you in."
- "You're signed in, but I do not see an active plan yet."
- "Everything looks ready. Let's connect."

## Sign In

If the user already has an access token or subscription URL, let the CLI handle it:

```bash
freeguard login --token <token> --json
```

or:

```bash
freeguard login --url <subscription_url> --json
```

If the user wants email sign-in, ask before sending the code:

> I can send a verification code to your email. Is that OK?

After the user confirms:

```bash
freeguard login --email <email> --send-code --json
```

Ask the user to enter the code directly into the CLI flow when possible. If a non-interactive command is required:

```bash
freeguard login --email <email> --code <code> --json
```

After a successful login, tell the user their login state is stored locally by the FreeGuard CLI.

## Subscription

Check account status first:

```bash
freeguard subscribe info --json
```

If no active plan is available, list plans:

```bash
freeguard subscribe list --json
```

Explain that FreeGuard VPN requires an external paid plan and show the plan names and prices returned by the CLI. Before creating a checkout session, ask:

> I can open the FreeGuard checkout page for the plan you chose. Is that OK?

After the user confirms:

```bash
freeguard subscribe create --plan <price_id> --email <email> --json
```

The user completes payment in the browser. After they say payment is complete, check status:

```bash
freeguard subscribe info --json
```

For account management, use the CLI-provided portal command only after the user asks to manage billing:

```bash
freeguard subscribe portal --email <email> --code <code>
```

## Connect

Default to the standard non-elevated connection:

```bash
freeguard connect --json
```

If the user requests a specific country, use the country code form:

```bash
freeguard connect US --json
```

If the user requests a city or server, list nodes first:

```bash
freeguard node list --json
```

Then use the short alias returned by the CLI:

```bash
freeguard connect la2 --json
```

Report the result in simple terms:

- Connected: mention the selected location and that the VPN is on.
- Subscription expired: guide the user to "Subscription".
- Login required: guide the user to "Sign In".
- Other failure: run diagnostics with `freeguard doctor --json` and summarize the actionable issue.

## Advanced Optional Mode

System-wide protection may require the operating system to show an administrator prompt because it changes low-level network routing. Only use this path when the user explicitly asks to protect every app or enable TUN mode.

Explain the tradeoff first:

> Standard mode protects apps that use the system proxy. System-wide mode can protect more traffic, but your computer may ask for administrator approval. Would you like to try system-wide mode?

If the user confirms, run only the CLI command and let the CLI or operating system manage any permission prompt:

```bash
freeguard connect --tun --json
```

If the user declines or the command fails because permission was denied, fall back to standard mode:

```bash
freeguard connect --json
```

## Daily Usage

Use these commands when the user asks for routine help:

| User intent | Command |
| --- | --- |
| Check status | `freeguard status --json` |
| Connect | `freeguard connect --json` |
| Disconnect | `freeguard disconnect --json` |
| Reconnect | `freeguard reconnect --json` |
| Show servers | `freeguard node list --json` |
| Test servers | `freeguard node test --all --json` |
| Check plan | `freeguard subscribe info --json` |
| Troubleshoot | `freeguard doctor --json` |
| Sign out | `freeguard disconnect --json` then `freeguard logout --json` |

## Troubleshooting

When something fails, run:

```bash
freeguard doctor --json
```

Interpret the output for the user:

- Network issue: ask them to check the current internet connection.
- Login issue: guide them through "Sign In".
- Subscription issue: guide them through "Subscription".
- Port conflict: explain that FreeGuard can choose another local proxy port.
- Core component issue: tell them the CLI needs to repair a local VPN component and follow the CLI's prompt.

## Language Guide

Prefer these user-facing terms:

| Technical term | Friendly wording |
| --- | --- |
| TUN mode | system-wide protection |
| node | server |
| node alias | short server name |
| rule mode | smart routing |
| mihomo | VPN engine |
| config file | settings |
| credentials file | local login state |

---
name: get-my-ip
description: Get the machine's current public IP address by calling `curl ifconfig.me`. Use when the user asks for their IP address, public IP, external IP, or explicitly wants to use ifconfig.me.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://github.com/hilaraklesantosw-art/skills
---

# Get My IP

Use this skill when the user wants the current machine's IP address as seen from the public internet.

This skill uses:

```bash
curl -fsSL ifconfig.me
```

## Outcome

Return the current public IP address from `ifconfig.me`.

Keep the answer concise. By default, return only the IP unless the user asks for more detail.

## Workflow

### 1. Clarify the meaning only when needed

`ifconfig.me` returns the public outbound IP, not the local LAN IP.

If the user says "local IP" but also asks to use `ifconfig.me`, follow the request and, when useful, note that the result is the public IP.

### 2. Run the command

Use:

```bash
curl -fsSL ifconfig.me
```

Do not replace it with another service unless the user asks for a fallback.

### 3. Return the result

If successful:

- return the IP directly

If it fails:

- say the public IP could not be retrieved
- include the brief reason when available, such as missing `curl`, network failure, or service unavailability

## Scope Boundaries

This skill is only for retrieving the public IP via `ifconfig.me`.

It is not for:

- finding the local LAN IP
- diagnosing network routing issues
- checking multiple interfaces
- performing geolocation lookups

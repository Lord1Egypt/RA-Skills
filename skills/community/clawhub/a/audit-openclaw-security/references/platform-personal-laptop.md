# Platform playbook: Personal laptop (macOS / Windows / Linux)

## Why laptops are special

- They roam across networks.
- They often hold personal data, browser sessions, and development secrets.
- They are more likely to run other untrusted tools or experiments locally.

## Preferred pattern

- Do not run OpenClaw 24/7 on your primary laptop unless there is a strong reason.
- Prefer isolation:
  - Docker with careful mounts and networking
  - a VM
  - a separate OS user with minimal access to your personal files

## Audit checks

1. Is the Gateway loopback-bound?
2. Is auth enabled?
3. Are DMs locked down with pairing/allowlists?
4. Are groups mention-gated?
5. Are runtime/fs/elevated tools constrained?
6. Is transcript/log retention intentional?

## Hardening actions

### Common to all laptops

- keep the Gateway local-only
- avoid running the bot on untrusted networks
- turn it off when you do not need it
- prefer `session.dmScope: "per-channel-peer"` for any multi-user scenario
- start from a conservative tool profile

### macOS laptops

- same guidance as the Mac mini playbook, with extra emphasis on travel and untrusted Wi-Fi
- FileVault and the macOS firewall should both be on

### Windows laptops

- prefer WSL2 for shell-driven audit and management flows
- keep Defender and BitLocker enabled
- keep the WSL distro updated and minimal

### Linux laptops

- use a host firewall (`ufw` / `nftables`)
- consider a dedicated user or container boundary for OpenClaw

## Verification

```bash
openclaw security audit --deep --json
openclaw gateway probe --json
openclaw channels status --probe
```

Confirm there is no inbound exposure beyond localhost or your intentional tailnet path.

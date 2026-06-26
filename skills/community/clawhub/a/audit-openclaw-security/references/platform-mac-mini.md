# Platform playbook: Mac mini or other always-on macOS host

## Threat assumptions

- The host lives on a home or office LAN.
- Local networks are not automatically trustworthy: guest Wi-Fi, IoT devices, and shared machines matter.
- macOS hosts often have rich personal data, browser sessions, and other credentials.

## Audit checks

1. Gateway should normally be **loopback-bound**.
2. Gateway auth should be enabled.
3. Control UI device-auth bypass should be **off**.
4. Discovery should be `minimal` or `off` unless there is a specific reason otherwise.
5. File permissions on OpenClaw state/config should be user-only.
6. Transcript/log retention should be intentional.

Useful commands:

```bash
openclaw security audit --deep --json
openclaw gateway probe --json
lsof -nP -iTCP -sTCP:LISTEN
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
fdesetup status || true
```

## Hardening actions

### 1) Separate the bot from your main user

Best practice is a dedicated macOS user for OpenClaw with:

- no iCloud login
- no broad access to personal documents
- only the permissions/features the bot actually needs

### 2) Disk and OS security

- enable FileVault
- keep macOS updated
- keep the application firewall on
- use stealth mode when it fits the host’s role

### 3) Remote access

Preferred options:

- SSH tunnel to `127.0.0.1:18789`
- Tailscale Serve

Avoid:

- router port-forwarding
- Tailscale Funnel for the Gateway
- arbitrary reverse proxies without `trustedProxies` and explicit origins

### 4) Tailscale Serve nuance

`gateway.auth.allowTailscale` can allow tokenless Control UI/WebSocket auth via Tailscale identity headers. That assumes the host itself is trusted.

If the macOS host also runs untrusted local code, or if another reverse proxy sits in front of the Gateway, disable `gateway.auth.allowTailscale` and require normal auth.

### 5) Tool and browser minimisation

- start from `tools.profile: "messaging"` for inbox-facing bots
- treat browser control as operator access
- keep runtime/fs/elevated tools off unless there is a narrow reason

## Verification

- `openclaw security audit --deep --json` shows no critical findings
- `openclaw gateway probe --json` matches the intended local/tailnet target
- listener checks show 18789 on loopback only unless there is a deliberate exception

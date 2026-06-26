# Platform playbook: AWS EC2 (or similar cloud VM)

## Threat assumptions

- Public cloud instances are scanned constantly.
- Misconfigured security groups, public IPs, and reverse proxies are common.
- A compromise can expose cloud credentials, bot credentials, and any attached storage.

## Preferred deployment pattern

- Put the instance in a **private subnet** with no public IPv4 when possible.
- Access it via:
  - AWS Systems Manager Session Manager, or
  - SSH from a tightly controlled source, or
  - VPN / Tailscale
- Keep the OpenClaw Gateway bound to **loopback**.
- If you need remote access, prefer Tailscale Serve or an SSH tunnel. Do **not** expose port 18789 directly.

## Audit checks

1. **Security groups / firewall**
   - confirm no inbound `18789/tcp` from `0.0.0.0/0` or wide CIDRs
   - keep SSH tightly restricted, or disable it and use SSM

2. **Gateway exposure**
   - `gateway.bind` should normally be `loopback`
   - `openclaw gateway probe --json` should show the intended target, not an accidentally public listener

3. **Reverse proxies**
   - if nginx/Caddy/Traefik fronts the Gateway, configure `gateway.trustedProxies`
   - keep `gateway.allowRealIpFallback: false` unless you absolutely need it
   - for non-loopback Control UI, set `gateway.controlUi.allowedOrigins`

4. **Cloud metadata and IAM**
   - prefer IMDSv2
   - keep IAM role permissions minimal
   - think about SSRF risk if runtime/web tools are enabled

5. **Storage and logs**
   - encrypt attached volumes
   - set log retention intentionally
   - treat `~/.openclaw` and transcripts as sensitive application data

## OpenClaw-specific cloud guidance

- keep DM pairing on; do not run shared inboxes with broad tools
- disable or minimise mDNS discovery (`minimal` or `off`)
- do not publish browser control or node-management surfaces publicly
- if running in Docker, also apply `platform-docker.md`

## Verification

```bash
openclaw security audit --deep --json
openclaw gateway probe --json
openclaw channels status --probe
```

Also test from an external network that port 18789 is not reachable.

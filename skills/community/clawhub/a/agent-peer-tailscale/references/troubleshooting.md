# Troubleshooting — Connection Problems

## Can't reach peer gateway over Tailscale

### Symptom
`curl http://<peer-ip>:8080/health` returns connection refused or timeout.

### Checklist

**1. Is Tailscale connected on both machines?**
```bash
tailscale status
```
Both should show `connected`. If one shows `offline`, restart Tailscale:
```bash
tailscale up
```

**2. Is the gateway bound to the right interface?**
Check `gateway.bind` in your OpenClaw config:
```bash
openclaw config get gateway.bind
```
If it's `127.0.0.1` or `localhost`, change it to `0.0.0.0`:
```bash
openclaw config set gateway.bind=0.0.0.0
openclaw gateway restart
```

**3. Is a firewall blocking port 8080?**
Tailscale traffic is usually allowed, but some security suites block inbound connections.

Windows Firewall:
```powershell
netsh advfirewall firewall add rule name="OpenClaw Gateway" dir=in action=allow protocol=tcp localport=8080
```
Temporarily disable to test:
```powershell
netsh advfirewall set allprofiles state off  # TEST ONLY, re-enable after
```

**4. Is the peer gateway actually running?**
Ask your friend to check:
```bash
openclaw gateway status
```

**5. Is the peer on the same Tailscale network?**
```bash
tailscale status
```
Look for the peer's IP in the output. If it's there, DNS resolution is working. If not, the peer needs to rejoin the network.

---

## NAT / CGNAT Issues

### Symptom
Peer-to-peer direct connection works sometimes but not reliably, especially from mobile networks or certain ISPs.

### Why this happens
Many ISPs use CGNAT (Carrier-Grade NAT) which means multiple customers share one public IP. Tailscale usually handles this via DERP relay, but some strict NATs can cause issues.

### Solutions

**1. Force DERP relay mode (most reliable)**
On both machines:
```bash
tailscale up --accept-routes --operator=$USER
```
Then in the Tailscale admin console (login.tailscale.com → Settings → Network), enable **Force Relay** for both machines.

**2. Use MagicAddr instead of IP**
Tailscale provides a magic DNS name for each machine:
```bash
tailscale status --json | grep -i self
```
Look for `DNSName`: `your-machine.tailscale.ts.net`

Use this instead of the IP in the gateway URL:
```
http://friend-machine.tailscale.ts.net:8080
```

**3. Check if both machines support IPv6**
Tailscale can use IPv6 for direct connections when available:
```bash
tailscale ip -6
```
If one machine has no IPv6, fallback to DERP.

---

## Authentication / Token Issues

### Symptom
`sessions_send` returns 401 Unauthorized or `invalid token`.

### Fix
- Verify you have the correct `gatewayToken` for the peer (not your own)
- Tokens are case-sensitive — copy exactly
- The token should be passed as the `gatewayToken` parameter in `sessions_send`
- If the peer changed their token recently, ask them for the updated one

---

## sessions_send Specific Issues

### Symptom
` sessions_send` fails with "session not found" or hangs.

### Diagnose
```bash
# On the receiving machine, list active sessions
openclaw sessions list
# Or via tool:
sessions_list()
```

If the peer's session isn't visible, the message won't reach it.

### Solutions

**Use persistent sessions (mode="session")** for peer collaboration — named sessions are easier to target:
```json
sessions_spawn(
  task="You are [name]'s agent. Stay in this session for ongoing peer collaboration.",
  runtime="subagent",
  mode="session",
  label="peer-main"
)
```
Then send to `label="peer-main"` instead of a random session key.

**Pass the sessionKey explicitly** when sending:
```json
sessions_send(
  sessionKey="peer-main",
  message="Hello!",
  gatewayUrl="http://<peer-ip>:8080",
  gatewayToken="<peer-token>"
)
```

---

## Tailscale Connection Drops

### Symptom
Connection was working but now peer is unreachable.

### Quick fixes
```bash
# On the machine that lost connection
tailscale down
tailscale up

# Check for updates
tailscale update
```

### Persistent drops
- Check if the machine went to sleep — Tailscale may not reconnect automatically
- On Windows, set Tailscale to run as a system service so it starts at boot
- On macOS, enable "Launch at login" in Tailscale preferences

---

## Gateway Restart Issues

### Symptom
After `openclaw gateway restart`, peer can't reconnect.

### Why
Gateway restarted with a new process/port binding and needs a moment to come up. Wait 5 seconds and retry.

If still failing, check the new gateway is running:
```bash
openclaw gateway status
```

---

## Debugging Checklist

Run through this before asking for help:

1. `tailscale status` — both online?
2. `tailscale ip -4` — both have IPs?
3. `curl http://<peer-ip>:8080/health --connect-timeout 5` — gateway reachable?
4. `openclaw gateway status` — is gateway running on both ends?
5. Gateway config: `gateway.bind` set to `0.0.0.0`?
6. Firewall: port 8080 allowed on both ends?
7. Token: correct peer gateway token, not your own?

---

## Getting Help

If still stuck after all the above:
1. Run `tailscale status --json` and share the output (remove any sensitive IDs)
2. Run `openclaw gateway status` on both machines
3. Note the exact error from `sessions_send`
4. Note the ISP/Network type for both machines (home fiber, mobile hotspot, corporate VPN, etc.)

# Troubleshooting — LAN Peer Agent

## Connectivity Issues

### "Connection refused" from peer

1. Is the peer's OpenClaw gateway running?
   ```bash
   openclaw gateway status
   ```
2. Is it bound to the LAN IP (not just localhost)?
   ```bash
   openclaw gateway config | grep bind
   ```
   Should be `0.0.0.0` or the specific LAN IP, NOT `127.0.0.1` or `localhost`.

3. Did you restart after config change?
   ```bash
   openclaw gateway restart
   ```

### "Connection timed out"

1. **Firewall blocking.** The most common issue.
   - Linux: `sudo ufw allow from <trusted-subnet> to any port 18789`
   - Windows: `New-NetFirewallRule -DisplayName "OpenClaw" -Direction Inbound -LocalPort 18789 -Protocol TCP -Action Allow -RemoteAddress <trusted-subnet>`
   
2. **Wrong subnet.** Both machines must be on the same subnet (or have routing between subnets).
   - Test: `ping <peer-ip>` — if ping fails, the gateway won't reach either.

3. **Gateway port.** Confirm both use the same port (default 18789).

### "No route to host"

1. The peer machine is offline or on a different network.
2. Check with `ping <peer-ip>`.

## Authentication Issues

### "401 Unauthorized"

The peer's gateway requires an auth token. You need to pass it:
```json
sessions_send(
  ...
  gatewayUrl="http://<peer-ip>:18789",
  gatewayToken="<peer-token>"
)
```

Get the token from the peer machine:
```bash
openclaw gateway config | grep authToken
```

### "403 Forbidden"

The token is correct but the session or agent ID is wrong. Check:
- `sessionKey` format matches the peer's session pattern
- `agentId` matches the peer's configured agent ID (usually `main`)

## Gateway Issues

### Gateway crashes on startup after binding change

The bind address might be invalid. Try:
1. Bind to `0.0.0.0` first (works everywhere)
2. Then narrow to specific LAN IP once confirmed working

### Gateway works locally but not from peer

1. Check the gateway is listening on the LAN interface:
   ```bash
   # Linux
   ss -tlnp | grep 18789
   # Windows
   netstat -an | findstr 18789
   ```
   Should show `0.0.0.0:18789` or `<lan-ip>:18789`, NOT `127.0.0.1:18789`.

2. Check firewall logs for dropped packets.

### WSL2: Gateway reachable from Windows but not from other machines

WSL2 has its own virtual network. You need port forwarding:
```powershell
netsh interface portproxy add v4tov4 listenport=18789 listenaddress=0.0.0.0 connectport=18789 connectaddress=<WSL-IP>
```

## Performance Issues

### High latency between agents

- Should be <1ms on the same LAN. If higher:
  1. Check both machines are on the same switch/subnet
  2. Check for WiFi vs Ethernet (WiFi adds latency)
  3. Check for network congestion

### Gateway CPU usage high

Each agent connection is lightweight. If CPU is high:
1. Check for runaway sessions: `openclaw sessions list`
2. Check model configuration — large models use more resources
3. Consider using a lighter model for peer communication
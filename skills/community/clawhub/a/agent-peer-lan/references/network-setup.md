# Network Setup — LAN Peer Agent

## Common Network Topologies

### Two machines on the same subnet
Simplest setup. Both machines on e.g. 192.168.1.0/24.

```
Machine A: 192.168.1.10 (gateway on :18789)
Machine B: 192.168.1.20 (gateway on :18789)
```

Just bind each gateway to `0.0.0.0` or the LAN IP, add firewall rules, done.

### Two machines on different subnets
If you have a router between subnets (e.g., IoT on .1.x, trusted on .42.x), ensure the router allows traffic between the two subnets on the gateway port.

For example, with iptables on the router:
```bash
iptables -A FORWARD -s 192.168.1.0/24 -d 192.168.2.0/24 -p tcp --dport 18789 -j ACCEPT
iptables -A FORWARD -s 192.168.2.0/24 -d 192.168.1.0/24 -p tcp --dport 18789 -j ACCEPT
```

### Docker / WSL considerations
If OpenClaw runs inside Docker or WSL, the gateway may only be reachable via the host's IP. Set up port forwarding:

**WSL2:**
```powershell
netsh interface portproxy add v4tov4 listenport=18789 listenaddress=0.0.0.0 connectport=18789 connectaddress=<WSL-IP>
```

**Docker:**
```bash
docker run -p 18789:18789 ...  # map the port to the host
```

## Gateway Binding

### Option A: Bind to all interfaces (`0.0.0.0`)
```json
{ "gateway": { "bind": "0.0.0.0", "port": 18789 } }
```
Easiest, but the gateway is reachable from ALL network interfaces. Use firewall rules to restrict access.

### Option B: Bind to specific LAN IP
```json
{ "gateway": { "bind": "192.168.1.10", "port": 18789 } }
```
More secure — gateway only reachable on that specific interface. Must change if your LAN IP changes.

## DNS / mDNS
Consider adding host entries to `/etc/hosts` (Linux) or `C:\Windows\System32\drivers\etc\hosts` (Windows) so you can use hostnames instead of IPs:

```
192.168.1.10    server-agent
192.168.1.20    pc-agent
```

This makes peer configs more readable and resilient to IP changes.
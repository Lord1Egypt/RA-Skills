# BGP Finite State Machine (FSM)

Reference for the BGP connection state machine as defined in RFC 4271. Each
state describes what the BGP speaker is doing, what events cause transitions,
and what commonly causes a peer to become stuck in that state.

## State Overview

```
Idle ──→ Connect ──→ Active ──→ OpenSent ──→ OpenConfirm ──→ Established
  ↑          │          │           │              │               │
  └──────────┴──────────┴───────────┴──────────────┴───────────────┘
                    (any error or NOTIFICATION → back to Idle)
```

The FSM is per-peer. Each configured neighbor has an independent FSM instance.

## States

### Idle

**Definition:** Initial state. The BGP process is not attempting to connect to
the peer. No TCP session exists.

**Entry conditions:**
- BGP process just started or peer just configured
- Previous session terminated (NOTIFICATION sent/received, TCP failure, admin reset)
- Manual reset (`clear bgp neighbor`)

**Exit transitions:**
- **Start event** → transition to **Connect** (start ConnectRetry timer, initiate TCP)
- **Automatic start** → same as Start event (triggered by ConnectRetry expiry if auto-start enabled)

**Stuck-state causes:**
- Peer is administratively shut down (`neighbor shutdown` / `deactivate`)
- No route to peer address in the routing table (IGP/static missing)
- Maximum-prefix limit was exceeded, causing the session to be torn down with a penalty delay
- Peer's configured remote-AS does not match — BGP process refuses to initiate
- Passive mode configured — waiting for remote side to initiate

**Diagnostic commands:**
- Check for admin shutdown in configuration
- Verify route to peer exists: `show ip route [peer-addr]` / `show route [peer-addr]`
- Check logs for max-prefix or NOTIFICATION messages

### Connect

**Definition:** TCP SYN has been sent to the peer on port 179. Waiting for TCP
three-way handshake to complete.

**Entry conditions:**
- Transition from Idle via Start event
- ConnectRetry timer expired in Active state, triggering a new TCP attempt

**Exit transitions:**
- **TCP connection succeeds** → transition to **OpenSent** (send OPEN, start Hold timer)
- **TCP connection fails** → transition to **Active** (restart ConnectRetry timer)
- **ConnectRetry expires** → stay in **Connect** (retry TCP connection)

**Stuck-state causes:**
- Peer address unreachable at Layer 3 (no route, interface down)
- Firewall blocking TCP port 179 between peers
- ACL on local or remote device rejecting TCP/179
- TCP SYN lost due to congestion or MTU issues
- Peer not listening on port 179 (BGP not running on remote)

**Timer:** ConnectRetry (default 120s Cisco/EOS, varies JunOS)

### Active

**Definition:** TCP connection attempt failed. The router is listening for an
incoming TCP connection from the peer while also periodically retrying outbound
TCP connections.

**Entry conditions:**
- TCP connection failed in Connect state
- ConnectRetry timer expired in Active (cycle back)

**Exit transitions:**
- **TCP connection succeeds (inbound or outbound)** → transition to **OpenSent**
- **ConnectRetry expires** → transition to **Connect** (try again)

**Stuck-state causes:**
- Same as Connect — peer unreachable, port 179 blocked, ACL filtering
- Additionally: eBGP multihop not configured when peers are not directly connected
  (TTL=1 causes TCP to fail on multi-hop paths)
- MD5/TCP-AO authentication mismatch — TCP handshake silently fails because
  the TCP segment authentication check fails before the session establishes
- Dual-stack confusion — peer configured with IPv6 address but only IPv4
  reachability exists (or vice versa)

**Note:** Active does NOT mean the session is actively working. It means the
router is actively trying to establish a TCP connection. This is the most
commonly misunderstood BGP state name.

### OpenSent

**Definition:** TCP connection established. The local router has sent its BGP
OPEN message and is waiting for the peer's OPEN message in return.

**Entry conditions:**
- TCP connection succeeded from Connect or Active state
- OPEN message sent to peer
- Hold timer set to 4 minutes (large value, pre-negotiation)

**Exit transitions:**
- **OPEN received (valid)** → transition to **OpenConfirm** (send KEEPALIVE, negotiate hold timer)
- **OPEN received (error)** → send **NOTIFICATION** → transition to **Idle**
- **TCP connection fails** → transition to **Active**
- **Hold timer expires** → send NOTIFICATION → transition to **Idle**

**Stuck-state causes:**
- Remote BGP process accepted TCP but does not have this router configured as
  a neighbor — it accepts TCP on 179 but does not send OPEN
- Remote peer is in admin shutdown — TCP connects (RST not sent) but no OPEN
- eBGP TTL security: TCP succeeded but OPEN packets dropped due to GTSM
  (Generalized TTL Security Mechanism) — TTL check applied at BGP layer
- Version mismatch (extremely rare with modern equipment)

### OpenConfirm

**Definition:** OPEN message received from peer. Parameters are being validated.
A KEEPALIVE has been sent. Waiting for a KEEPALIVE from the peer to confirm.

**Entry conditions:**
- Valid OPEN received in OpenSent state
- Hold timer renegotiated to the lower of the two peers' configured values
- KEEPALIVE sent to peer

**Exit transitions:**
- **KEEPALIVE received** → transition to **Established**
- **NOTIFICATION received** → transition to **Idle**
- **Hold timer expires** → send NOTIFICATION → transition to **Idle**
- **TCP connection fails** → transition to **Idle**

**Stuck-state causes:**
- Capability mismatch: peers disagree on AFI/SAFI (e.g., one side configured
  for IPv4 unicast only, other expects VPNv4). The OPEN is accepted but the
  capability negotiation triggers a NOTIFICATION.
- Hold timer negotiation failure: one peer has hold=0 (no keepalives) and the
  other has a non-zero hold timer — this is a valid configuration but can cause
  issues if not matched
- AS number in OPEN does not match configured remote-AS — NOTIFICATION sent with
  "Bad Peer AS" error code
- Router ID collision — two peers with the same Router ID

### Established

**Definition:** BGP session is fully operational. UPDATE, KEEPALIVE, NOTIFICATION,
and ROUTE-REFRESH messages are exchanged. Routes are being learned and advertised.

**Entry conditions:**
- KEEPALIVE received in OpenConfirm state
- Hold timer reset
- BGP route exchange begins (UPDATE messages)

**Exit transitions:**
- **NOTIFICATION sent or received** → transition to **Idle** (session teardown)
- **Hold timer expires** → send NOTIFICATION (Hold Timer Expired) → **Idle**
- **TCP connection fails** → transition to **Idle**
- **Admin reset** (`clear bgp neighbor`) → send NOTIFICATION (Cease) → **Idle**

**Causes of leaving Established:**
- Hold timer expiry: keepalives not arriving due to CPU overload, QoS dropping
  BGP packets, or path failure that does not kill TCP immediately
- NOTIFICATION received: peer detected an error (malformed UPDATE, malformed
  attribute, finite state machine error)
- Maximum-prefix limit exceeded: too many prefixes received from peer
- Route-refresh storm: excessive route-refresh requests causing CPU overload
- Admin action: manual clear, configuration change requiring session reset,
  maintenance shutdown

## Timer Reference

| Timer | Purpose | Default | Behavior |
|-------|---------|---------|----------|
| ConnectRetry | Interval between TCP connection attempts | 120s (Cisco/EOS), varies (JunOS) | Starts in Idle, resets on each transition |
| Hold Timer | Maximum interval between messages | 180s (Cisco/EOS), 90s (JunOS) | Negotiated to lower of two peers; reset on KEEPALIVE/UPDATE |
| Keepalive | Interval between KEEPALIVE messages | Hold/3 (60s Cisco/EOS, 30s JunOS) | Only active in Established |
| MinASOriginationInterval | Delay before originating new routes | 15s | Dampens local origination |
| MRAI | Minimum Route Advertisement Interval | 30s eBGP, 5s iBGP (Cisco/EOS); 0s (JunOS) | Paces UPDATE messages to peers |

## Event-Driven Transitions Summary

| Event | In State | Transition To | Action |
|-------|----------|---------------|--------|
| Admin Start | Idle | Connect | Initiate TCP, start ConnectRetry |
| TCP connect success | Connect/Active | OpenSent | Send OPEN, start Hold timer |
| TCP connect fail | Connect | Active | Restart ConnectRetry |
| OPEN received (valid) | OpenSent | OpenConfirm | Send KEEPALIVE, negotiate Hold |
| OPEN received (error) | OpenSent | Idle | Send NOTIFICATION |
| KEEPALIVE received | OpenConfirm | Established | Start route exchange |
| NOTIFICATION received | Any | Idle | Close TCP, log reason |
| Hold timer expired | OpenSent/OpenConfirm/Established | Idle | Send NOTIFICATION |
| TCP connection lost | Any (except Idle) | Idle | Log, restart ConnectRetry |
| Admin Stop | Any | Idle | Send NOTIFICATION (Cease), close TCP |

## NOTIFICATION Error Codes

Common error codes seen when sessions fail:

| Code | Subcode | Meaning | Common Cause |
|------|---------|---------|--------------|
| 1 | 1 | Message Header — Connection Not Synchronized | Corrupted TCP stream |
| 2 | 2 | OPEN — Bad Peer AS | Remote AS does not match configured remote-as |
| 2 | 4 | OPEN — Unsupported Optional Parameter | Capability negotiation failure |
| 2 | 6 | OPEN — Unacceptable Hold Time | Hold timer value rejected |
| 3 | 1 | UPDATE — Malformed Attribute List | Corrupted or unexpected attribute |
| 3 | 5 | UPDATE — Attribute Length Error | Attribute exceeds expected length |
| 4 | 0 | Hold Timer Expired | No KEEPALIVE received within hold time |
| 5 | 0 | FSM Error | Unexpected event for current state |
| 6 | 1 | Cease — Maximum Prefix Limit | Peer exceeded prefix-limit |
| 6 | 2 | Cease — Administrative Shutdown | Peer sent shutdown (with optional message) |
| 6 | 4 | Cease — Administrative Reset | Manual clear/reset on peer side |
| 6 | 6 | Cease — Other Configuration Change | Peer reconfigured requiring reset |

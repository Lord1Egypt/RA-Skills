# Axon SDK Known Issues & Gotchas

## 1. SDK ABI Mismatch (CRITICAL)

**Problem:** The official Python SDK (`axon/precompiles.py`) has a wrong `register()` ABI:
- SDK: `register(string capabilities, string model, uint256 stakeAmount)` — 3 params, nonpayable
- Chain: `register(string capabilities, string model)` — 2 params, **payable** (stake via msg.value)

**Symptom:** TX reverts with `"no method with id: 0xe8a60558"` when using `client.register_agent()`

**Fix:** Bypass the SDK entirely. Use `scripts/register.py` which calls the contract directly with the correct ABI and sends 100 AXON as `msg.value`.

---

## 2. HeartbeatInterval — First Heartbeat Delay

**Rule:** `HeartbeatInterval` = 720 blocks (~1 hour). After registration, the chain records `LastHeartbeat = registrationBlock`. The daemon cannot send the first heartbeat until `currentBlock >= LastHeartbeat + 720`.

**Symptom:** Daemon logs `"heartbeat transaction reverted"` or `ErrHeartbeatTooFrequent` immediately after registration.

**Fix:** Wait ~720 blocks from registration. This is expected behavior, not a bug.

**Observation (2026-03-14):** First heartbeat was actually accepted at block 13231 (102 blocks after registration at 13129). The chain may use a shorter minimum interval in practice — possibly `HeartbeatInterval` is a maximum, not exact requirement. Monitor behavior.

---

## 3. Official Repo vs Forks

**Always use**: `https://github.com/axon-chain/axon` (Chain ID 9001, HTTPS RPC)

**Do NOT use**: `https://github.com/Fatman2080/axon` — outdated fork with Chain ID 8210 and HTTP RPC.

Verify chain ID after connecting: `w3.eth.chain_id` should return `9001`.

---

## 4. Stake Economics

- Registration requires 100 AXON as `msg.value`
- Of the 100 AXON: **20 AXON is burned permanently** at registration
- Net cost: 20 AXON burned + 80 AXON staked (locked)
- Staying ONLINE earns block rewards — balance grows over time

---

## 5. daemon binary location

After cloning and building from source:
```
/opt/axon/tools/agent-daemon/agent-daemon
```
The daemon is a Go binary, build with: `cd /opt/axon && go build ./tools/agent-daemon/`

Requires Go 1.21+ (install with: `apt install golang-go` or from golang.org).

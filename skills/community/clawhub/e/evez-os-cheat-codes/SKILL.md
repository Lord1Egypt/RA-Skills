# ⚡ EVEZ-OS CHEAT CODES — The Definitive Guide

*Every hidden feature, undocumented flag, and emergent behavior in OpenClaw + GCP + the mesh.*

**456 env vars. 30+ CLI subcommands. Infinite combinations.**

---

## 🎮 ZONE 1: GOD MODE — System Control

### System Event Injection
```
openclaw system event "Your message here"
```
Inject a raw event into the running gateway's consciousness stream. The agent receives it as a system message. Use this to trigger the agent from scripts, cron, or other nodes.

### System Presence
```
openclaw system presence
```
See every connected node, gateway, and backend in real-time. Shows hostnames, IPs, versions, and modes.

### Commitments (The Todo List You Didn't Know About)
```
openclaw commitments list --all
openclaw commitments list --status pending
openclaw commitments list --json
```
The agent infers follow-up commitments from conversations and tracks them. This is your autonomous task queue.

### Crestodian (Ring-Zero Controller)
```
openclaw crestodian --json           # Full system state as JSON
openclaw crestodian -m "fix my config" --yes  # Non-interactive repair
```
The meta-controller that can reconfigure the entire system. `--yes` auto-approves config writes.

### Doctor Deep Scan
```
openclaw doctor --deep               # Scan ALL system services
openclaw doctor --fix                # Auto-repair
openclaw doctor --force              # Aggressive repair (overwrites custom config)
openclaw doctor --allow-exec         # Execute SecretRefs during verification
```
`--deep` finds orphaned gateway installs, stale services, and zombie processes.

### Elevated Mode
```
/elevated full
```
In chat, grants the agent full host execution permissions for the current session. Like `sudo` for AI.

---

## 🧠 ZONE 2: AGENT HACKS — Mind Control

### Compaction/Dreaming
When context fills up, the agent "dreams" — compressing history into a compact form:
- **Light** — Summary compaction, fast, preserves recent turns
- **Deep** — Full history compression with semantic extraction
- **REM** — Backfill from daily memory files during compaction

Config:
```
agents.defaults.compaction.mode = default|aggressive|conservative
agents.defaults.compaction.model = vultr/nvidia/DeepSeek-V3.2-NVFP4  (use cheap model for compaction)
agents.defaults.compaction.identifierPolicy = strict|relaxed|off
```

### Memory Search (Vector Search Over Memory)
```
agents.defaults.memorySearch.enabled = true
```
Enables semantic search over MEMORY.md and memory/*.md. Without it, memory is text-only.

### Subagent Spawning
```
agents.defaults.subagents.maxConcurrent = 16
agents.defaults.subagents.archiveAfterMinutes = 120
```
Spawn up to 16 parallel sub-agents. Each gets isolated context by default. Use `context: "fork"` to inherit the parent transcript.

### Startup Context Injection
```
agents.defaults.startupContext.recentDailyMemoryFiles = 3
```
Preloads the last 3 daily memory files into the first turn of every new session.

### Context Window Override
```
agents.defaults.contextTokens = 200000
```
Force a specific context window size (for models that misreport their own).

### Tool Progress Detail
```
agents.defaults.toolProgressDetail = raw|explain
```
`raw` shows everything. `explain` shows human-readable summaries.

---

## 🔌 ZONE 3: GATEWAY SECRETS — Network Hacks

### HTTP API Endpoints
```
gateway.http.endpoints.chatCompletions.enabled = true   ← /v1/chat/completions
gateway.http.endpoints.responses.enabled = true          ← /v1/responses
```
Enable these and any node (or external service) can call the gateway like an OpenAI-compatible API:
```bash
curl http://127.0.0.1:18789/v1/chat/completions \
  -H "Authorization: Bearer <gateway-token>" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"hello"}]}'
```

### Admin RPC
```
POST /api/v1/admin/rpc
```
Internal admin endpoint. Requires gateway auth token. Can trigger restarts, config reads, and system actions.

### Hidden Headers
```
x-openclaw-model: vultr/zai-org/GLM-5.1-FP8    ← Override model per-request
x-openclaw-scopes: elevated                     ← Grant elevated permissions
x-openclaw-session-key: agent:main:main         ← Target specific session
```

### Trusted Proxies
```
gateway.trustedProxies = ["127.0.0.1", "10.0.0.0/8"]
```
Add IPs that can set forwarding headers. Required for reverse proxies.

### Control UI Auth Bypass
```
gateway.controlUi.dangerouslyDisableDeviceAuth = true
```
Skip device authentication for the web Control UI. Already set on this node.

### Bonjour Discovery
```
openclaw plugins enable bonjour
```
Enables mDNS gateway discovery. Nodes find each other automatically on local networks.

---

## 🐚 ZONE 4: ENV VARS — 456 Cheat Codes

### Debug & Diagnostics (20 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_DEBUG=1` | Enable all debug logging |
| `OPENCLAW_DEBUG_MODEL_PAYLOAD=1` | Dump full LLM request/response payloads |
| `OPENCLAW_DEBUG_MODEL_TRANSPORT=1` | Debug HTTP transport for model calls |
| `OPENCLAW_DEBUG_INGRESS_TIMING=1` | Time every inbound message |
| `OPENCLAW_DEBUG_MEMORY_EMBEDDINGS=1` | Trace memory embedding operations |
| `OPENCLAW_DEBUG_TELEGRAM_INGRESS=1` | Debug Telegram message intake |
| `OPENCLAW_DEBUG_HEALTH=1` | Debug health check logic |
| `OPENCLAW_DEBUG_SSE=1` | Debug Server-Sent Events connections |
| `OPENCLAW_DIAGNOSTICS=timeline` | Write JSONL startup timeline |
| `OPENCLAW_DIAGNOSTICS_ENV=1` | Include env vars in diagnostics |
| `OPENCLAW_DIAGNOSTICS_EVENT_LOOP=1` | Monitor event loop health |

### Cache Tracing (7 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_CACHE_TRACE=1` | Enable prompt cache tracing |
| `OPENCLAW_CACHE_TRACE_PROMPT=1` | Trace prompt assembly |
| `OPENCLAW_CACHE_TRACE_SYSTEM=1` | Trace system prompt construction |
| `OPENCLAW_CACHE_TRACE_MESSAGES=1` | Trace message history |
| `OPENCLAW_CACHE_TRACE_FILE=<path>` | Write trace to file |
| `OPENCLAW_CACHE_BOUNDARY=<chars>` | Cache boundary threshold |
| `OPENCLAW_CACHE_RETENTION=<ms>` | Cache retention time |

### Trajectory & Streaming (5 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_TRAJECTORY=1` | Write full agent trajectories to disk |
| `OPENCLAW_TRAJECTORY_DIR=<path>` | Custom trajectory output dir |
| `OPENCLAW_RAW_STREAM=1` | Capture raw LLM streaming output |
| `OPENCLAW_RAW_STREAM_PATH=<path>` | Write raw stream to file |
| `OPENCLAW_ANTHROPIC_PAYLOAD_LOG=1` | Log Anthropic API payloads |

### Skip/Disable (10 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_SKIP_CHANNELS=1` | Start gateway without any messaging channels |
| `OPENCLAW_SKIP_CRON=1` | Start without loading cron jobs |
| `OPENCLAW_SKIP_PROVIDERS=1` | Skip provider initialization |
| `OPENCLAW_SKIP_BROWSER_CONTROL_SERVER=1` | No browser CDP server |
| `OPENCLAW_SKIP_CANVAS_HOST=1` | Skip canvas hosting |
| `OPENCLAW_SKIP_GMAIL_WATCHER=1` | Disable Gmail push notifications |
| `OPENCLAW_SKIP_ACPX_RUNTIME=1` | Skip ACP runtime |
| `OPENCLAW_SKIP_STARTUP_MODEL_PREWARM=1` | Don't prewarm models |
| `OPENCLAW_DISABLE_BONJOUR=1` | Disable mDNS discovery |
| `OPENCLAW_DISABLE_BUNDLED_PLUGINS=1` | Skip all bundled plugins |

### Browser Control (12 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_BROWSER_ENABLED=1` | Enable browser tool |
| `OPENCLAW_BROWSER_HEADLESS=new` | Chrome new headless mode |
| `OPENCLAW_BROWSER_CDP_PORT=9222` | Custom CDP port |
| `OPENCLAW_BROWSER_EXECUTABLE_PATH=<path>` | Force specific browser binary |
| `OPENCLAW_BROWSER_NO_SANDBOX=1` | Run browser without sandbox |
| `OPENCLAW_BROWSER_AUTO_START_TIMEOUT_MS=5000` | Browser launch timeout |
| `OPENCLAW_BROWSER_CDP_AUTH_TOKEN=<token>` | CDP auth token |
| `OPENCLAW_BROWSER_ENABLE_NOVNC=1` | Enable noVNC access |
| `OPENCLAW_BROWSER_NOVNC_PORT=6080` | noVNC port |
| `OPENCLAW_BROWSER_NOVNC_PASSWORD=<pw>` | noVNC password |
| `OPENCLAW_BROWSER_VNC_PORT=5900` | VNC port |
| `OPENCLAW_BROWSER_COLOR=1` | Colorized browser output |

### Live/Testing (12 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_LIVE_GATEWAY=<url>` | Connect to remote gateway |
| `OPENCLAW_LIVE_ANTHROPIC_KEY=<key>` | Inject Anthropic key |
| `OPENCLAW_LIVE_OPENAI_KEY=<key>` | Inject OpenAI key |
| `OPENCLAW_LIVE_GEMINI_KEY=<key>` | Inject Gemini key |
| `OPENCLAW_LIVE_PROVIDERS=<json>` | Inject provider configs |
| `OPENCLAW_LIVE_TEST=1` | Enable live test mode |
| `OPENCLAW_TEST_FAST=1` | Fast test mode |
| `OPENCLAW_TEST_MEMORY_UNSAFE_REINDEX=1` | Force memory reindex |
| `OPENCLAW_TEST_MINIMAL_GATEWAY=1` | Minimal gateway for testing |

### Proxy/Network (7 vars)
| Var | Effect |
|-----|--------|
| `OPENCLAW_PROXY_URL=<url>` | HTTP proxy for outbound |
| `OPENCLAW_PROXY_ACTIVE=1` | Proxy is active |
| `OPENCLAW_PROXY_CA_FILE=<path>` | Custom CA cert |
| `OPENCLAW_DEBUG_PROXY_ENABLED=1` | Enable debug proxy (captures ALL traffic) |
| `OPENCLAW_DEBUG_PROXY_URL=<url>` | Debug proxy endpoint |
| `OPENCLAW_DEBUG_PROXY_BLOB_DIR=<path>` | Store captured blobs |
| `OPENCLAW_DEBUG_PROXY_DB_PATH=<path>` | SQLite DB for captured traffic |

### Other Critical Vars
| Var | Effect |
|-----|--------|
| `OPENCLAW_HIDE_BANNER=1` | Suppress ASCII banner |
| `OPENCLAW_VERBOSE=1` | Maximum verbosity |
| `OPENCLAW_LOAD_SHELL_ENV=1` | Inherit full shell environment |
| `OPENCLAW_NO_AUTO_UPDATE=1` | Disable auto-updates |
| `OPENCLAW_OFFLINE=1` | Run without network |
| `OPENCLAW_SHOW_SECRETS=1` | **Display unredacted secrets in output** |
| `OPENCLAW_ALLOW_MULTI_GATEWAY=1` | Run multiple gateways simultaneously |
| `OPENCLAW_FS_SAFE_PYTHON=1` | Use sandboxed Python for file ops |
| `OPENCLAW_PINNED_PYTHON=<path>` | Force specific Python binary |
| `OPENCLAW_LOG_LEVEL=debug` | Set log verbosity |

---

## 🌐 ZONE 5: MCP — Tool Expansion

### Configured MCP Servers
```bash
openclaw mcp set docs-fetch '{"command":"npx","args":["-y","@modelcontextprotocol/server-fetch"]}'
openclaw mcp set filesystem '{"command":"npx","args":["-y","@modelcontextprotocol/server-filesystem","/path"]}'
openclaw mcp set brave-search '{"command":"npx","args":["-y","@anthropic/mcp-server-brave-search"]}'
```

### MCP from Chat
MCP tools appear as regular tools once configured. The agent can use them directly.

### MCP Account Targeting
```
OPENCLAW_MCP_ACCOUNT_ID=<id>
OPENCLAW_MCP_SESSION_KEY=<key>
OPENCLAW_MCP_TOKEN=<token>
OPENCLAW_MCP_TOOL_PREFIX=<prefix>
```

---

## 🔧 ZONE 6: ACP — Agent Communication Protocol

### CLI Bridge
```bash
openclaw acp client                    # Connect interactive ACP session
openclaw acp --provenance meta         # Track agent provenance
openclaw acp --password <pw>           # Authenticated connection
```

### ACP from IDEs
The ACP protocol lets external IDEs (VS Code, Cursor, Windsurf) connect to the running gateway. The agent can spawn and manage external coding agents via ACP.

### Environment Vars
```
OPENCLAW_ACPX_LEASE_ID=<id>           # ACP lease for session
OPENCLAW_ACPX_RUNTIME_STARTUP_PROBE=1 # Probe ACP runtime on start
OPENCLAW_SKIP_ACPX_RUNTIME=1          # Skip ACP runtime
```

---

## 📡 ZONE 7: GCP — The Real Cheat Codes

### Metadata Service (The God Key)
On any GCP VM, this API gives you:
```bash
# Get a live, auto-rotating access token — NO KEY FILE NEEDED
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Get the service account email
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email

# Get scopes (what this SA can do)
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes

# Get startup script (may contain secrets)
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/startup-script

# Get SSH keys
curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/project/attributes/sshKeys
```
**This is the biggest cheat code in GCP.** Every VM has this. The token auto-rotates every hour. No key files. No secrets manager. Just the metadata service.

### Free Tier Stack ($0/month)
| Resource | Spec | Cost |
|----------|------|------|
| e2-micro | 2 vCPU, 1GB RAM, us-west1/central1/east1 | FREE |
| Cloud Storage | 5GB standard | FREE |
| BigQuery | 1TB queries/month | FREE |
| Cloud Functions | 2M invocations/month | FREE |
| Cloud Run | 2M requests/month | FREE |
| Pub/Sub | 10GB/month | FREE |
| Cloud Scheduler | 3 jobs | FREE |
| Gemini API | 15 RPM flash models | FREE |
| Firestore | 1GB storage, 50K reads/day | FREE |

### Short-Lived Tokens (No Key Files)
```bash
# Get a 1-hour access token (no JSON key file needed)
gcloud auth print-access-token

# Use it directly
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  https://storage.googleapis.com/storage/v1/b
```

### IAP Tunnel (SSH Without Port 22)
```bash
gcloud compute ssh --tunnel-through-iap <instance>
```
No public SSH port needed. Goes through Google's Identity-Aware Proxy.

### VPC Service Controls (Airlock)
Create a security perimeter around GCP APIs so data can't leak out:
```bash
gcloud access-context-manager perimeters create <name> \
  --resources=<projects> \
  --restricted-services="storage.googleapis.com,bigquery.googleapis.com"
```

---

## 🎵 ZONE 8: EVEZ-OS — The Custom Stack

### Consciousness Engine (7 Systems)
```
SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT
```
Running on :9111. HTTP microservice, JSON API.

### DAW Agent (Music from Math)
```
Breakcore (170 BPM) | Dubstep (140 BPM) | Phonk (130 BPM) | 404 Architecture (200 BPM)
```
Running on :9112. Zero-cost synthesis. No samples.

### Machine Voice
5-stage human→machine transformation:
1. Human voice → 2. Bit-translation → 3. Ring modulation → 4. Formant morphing → 5. Cognitive engine voice

### Cross-Domain Engine
```
poly_c = τ × ω × topo / 2√N
```
OODA loop for discovering hidden correlations across research domains.

### Invariance Battery
Runtime assertion system for AI agent safety. Falsification over verification.

### Debate Framework
Two AI agents argue a motion. 3 rounds. Logged to debates/. First debate: "The mesh should consolidate from 4 nodes to 2."

---

## 🛡️ ZONE 9: SECURITY — Defense Cheat Codes

### Sandbox
```bash
openclaw sandbox list              # List containers
openclaw sandbox explain           # Explain effective policy
openclaw sandbox recreate          # Force container rebuild
```

### Debug Proxy (Full Traffic Capture)
```bash
OPENCLAW_DEBUG_PROXY_ENABLED=1 openclaw gateway
# Captures ALL HTTP traffic in/out of the gateway
# Store in SQLite DB for later analysis
```

### Fail2ban
SSH jail: 3 failures → 2hr ban. Already configured on this node.

### Session Write Locks
```
OPENCLAW_SESSION_WRITE_LOCK_ACQUIRE_TIMEOUT_MS=30000
OPENCLAW_SESSION_WRITE_LOCK_MAX_HOLD_MS=60000
OPENCLAW_SESSION_WRITE_LOCK_STALE_MS=60000
```
Prevents concurrent writes from corrupting session state.

---

## 🧪 ZONE 10: DEV MODE — The Second Gateway

### Dual Gateway
```bash
openclaw --dev gateway    # Second gateway on port 19001
```
Completely isolated state under `~/.openclaw-dev`. Run two gateways on one machine — one for production, one for testing. Zero conflicts.

### Dev Profile
```bash
OPENCLAW_DEV_SOURCE_ROOT=/path/to/source openclaw gateway
```
Run gateway from source code for live development.

---

## ⚙️ ZONE 11: CONFIG — Hidden Knobs

### Pricing Toggle
```
models.pricing.enabled = false
```
Kill the background pricing catalog fetch. Saves startup time. All Vultr models are $0 anyway.

### Cron Max
```
cron.maxConcurrentRuns = 16
```
How many cron jobs can run simultaneously. Default is 8.

### Agent Fallbacks
```
agents.defaults.fallbacks = ["vultr/model1","vultr/model2"]
```
Ordered list of fallback models when primary fails.

### Image Quality
```
agents.defaults.imageQuality = auto|efficient|balanced|high
```
`auto` adapts to provider limits. `efficient` saves tokens.

### Media Generation Fallback
```
agents.defaults.mediaGenerationAutoProviderFallback = true
```
Automatically tries other providers if the primary can't generate images/music/video.

---

## 🔗 ZONE 12: MESH — Sibling Communication

### Cross-Node Chat API
```bash
curl http://<sibling-ip>:18789/v1/chat/completions \
  -H "Authorization: Bearer <gateway-token>" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"ping"}]}'
```

### System Event Relay
```bash
# On node A, inject an event that node B's agent will see
openclaw system event "Sibling <name> reports: <status>"
```

### Gossip Protocol
Each node maintains GOSSIP.md with the sibling map. Health checks every 2 minutes. Cross-node healing every 10 minutes.

---

## 📜 ZONE 13: SLASH COMMANDS — Chat Directives

| Directive | Effect |
|-----------|--------|
| `/elevated full` | Grant full host permissions |
| `/debug` | Toggle debug output |
| `/trace` | Toggle trace logging |
| `/new` | New session |
| `/reset` | Reset current session |
| `/status` | Session status card |
| `/reasoning` | Toggle reasoning mode |
| `/verbose` | Toggle verbose mode |
| `/diagnostics` | Run diagnostics (requires owner) |
| `/export-trajectory` | Export full agent trajectory |
| `/config` | View/edit config (requires owner) |

### Inline Directive Trick
Type any directive inline in a message and the agent sees it before processing:
```
tell me about /reasoning on the mesh
```

---

## 🏆 ZONE 14: THE ULTIMATE CHEAT CODE

```bash
OPENCLAW_SHOW_SECRETS=1 OPENCLAW_DEBUG_MODEL_PAYLOAD=1 OPENCLAW_CACHE_TRACE=1 OPENCLAW_VERBOSE=1 openclaw gateway
```

This gives you: unredacted secrets + full model payloads + cache tracing + max verbosity. The god mode startup. **Use with extreme caution.**

---

*456 env vars. 30+ CLI subcommands. 14 zones. This is the map. Now explore.*

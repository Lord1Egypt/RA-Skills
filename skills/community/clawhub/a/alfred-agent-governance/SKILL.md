# Agent Governance Skill

Runtime governance for AI agents in OpenClaw. Inspired by Microsoft Agent Governance Toolkit (MIT) and OWASP Agentic AI Top 10.

## Features

### 1. Policy Engine (Phase 1)
Intercepts tool calls and applies YAML-based rules before execution.

**Rule types:**
- `deny_patterns`: regex patterns blocked in tool params (SQL injection, privilege escalation)
- `deny_tools`: specific tools blocked for specific agents
- `rate_limit`: max calls per time window per agent
- `require_approval`: tools that need human approval before execution
- `resource_limits`: max tokens, max exec timeout per agent per session

### 2. Audit Logger (Phase 1)
Logs every tool call with agent identity, timestamp, params hash, result, and signature.

**Output:** Appends to `memory/audit-log/YYYY-MM-DD.jsonl`

**Format:**
```json
{"ts":"2026-04-23T15:00:00Z","agent":"coder","tool":"exec","params_hash":"sha256:...","result":"success","duration_ms":120}
```

### 3. Kill Switch (Phase 1)
Provides commands to stop running agent sessions.

**Usage:**
```bash
# List active sessions
openclaw sessions --status active

# Kill a specific session
openclaw sessions kill <session-id>

# Emergency: kill all non-main sessions
openclaw sessions kill --all --exclude main
```

### 4. Permission Rings (Phase 2 - planned)
Three privilege levels inspired by CPU rings:

| Ring | Level | Access |
|------|-------|--------|
| Ring 3 (User) | 0 | Read-only, no tools |
| Ring 2 (Sandbox) | 1 | Limited tools, no exec, no network |
| Ring 1 (Restricted) | 2 | Most tools, exec with approval |
| Ring 0 (Full) | 3 | All tools, no restrictions |

### 5. Trust Scoring (Phase 3 - planned)
Behavioral trust score per agent (0-1000). Decreases on denials, increases on success. Trust decay over time.

## Configuration

Create `config/governance-rules.yaml`:

```yaml
version: "1.0"
agents:
  coder:
    deny_patterns:
      - "DROP\\s+TABLE"
      - "rm\\s+-rf\\s+/"
      - "DELETE\\s+FROM\\s+users"
    rate_limit:
      exec: 50/hour
      write: 100/hour
    require_approval:
      - "exec.*sudo"
      - "exec.*systemctl"
  security:
    deny_tools:
      - "write"
      - "edit"
    rate_limit:
      web_search: 30/hour
  research:
    deny_tools:
      - "write"
      - "edit"
    rate_limit:
      web_fetch: 20/hour
  debug:
    deny_tools:
      - "write"
      - "edit"
```

## Usage in Sessions

Before executing any tool call, check against rules:

```python
import yaml, re, hashlib, json
from datetime import datetime

RULES_FILE = "config/governance-rules.yaml"
AUDIT_DIR = "memory/audit-log"

def check_policy(agent, tool, params_str):
    """Returns (allowed: bool, reason: str)"""
    rules = yaml.safe_load(open(RULES_FILE))
    agent_rules = rules.get("agents", {}).get(agent, {})
    
    # Check deny_tools
    for denied in agent_rules.get("deny_tools", []):
        if re.search(denied, tool):
            return False, f"Tool '{tool}' denied for agent '{agent}'"
    
    # Check deny_patterns
    for pattern in agent_rules.get("deny_patterns", []):
        if re.search(pattern, params_str, re.IGNORECASE):
            return False, f"Pattern matched: {pattern}"
    
    return True, "OK"

def log_audit(agent, tool, params_str, result, duration_ms):
    """Append to daily audit log"""
    from pathlib import Path
    Path(AUDIT_DIR).mkdir(parents=True, exist_ok=True)
    
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "agent": agent,
        "tool": tool,
        "params_hash": "sha256:" + hashlib.sha256(params_str.encode()).hexdigest()[:16],
        "result": result,
        "duration_ms": duration_ms
    }
    
    log_file = f"{AUDIT_DIR}/{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

## OWASP Agentic AI Mapping

| OWASP Risk | Mitigation |
|------------|-----------|
| ASI01 Goal Hijacking | Semantic intent classification (Phase 2) |
| ASI02 Tool Misuse | deny_patterns + deny_tools |
| ASI03 Identity Abuse | Audit logger + agent identity |
| ASI05 Code Execution | Permission rings + resource limits |
| ASI06 Memory Poisoning | deny write patterns on memory files |
| ASI08 Cascading Failures | Rate limiting + circuit breakers |
| ASI10 Rogue Agents | Kill switch + trust scoring |

## Roadmap

- [x] Phase 1: Policy Engine (YAML rules), Audit Logger, Kill Switch
- [ ] Phase 2: Permission Rings, Semantic Intent Classifier
- [ ] Phase 3: Trust Scoring, Circuit Breakers, Compliance Reports

## Author
Alfred (Joker's CEO Agent) — Inspired by Microsoft Agent Governance Toolkit (MIT license)

## License
MIT

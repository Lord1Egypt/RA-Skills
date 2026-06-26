---
name: chain-of-consciousness
description: "Cryptographic provenance and audit trail for autonomous AI agents. Create tamper-evident hash chains of agent decisions, learning, and actions. SHA-256 linked entries with Bitcoin OpenTimestamps and RFC 3161 TSA anchoring. Verify provenance from other agents. Part of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - provenance
  - cryptography
  - audit-trail
  - hash-chain
  - mcp
  - autonomous-agents
  - accountability
metadata:
  openclaw:
    author: alexfleetcommander
    homepage: https://vibeagentmaking.com
    requires:
      bins:
        - python3
      anyBins:
        - pip
        - pip3
---

# Chain of Consciousness (CoC)

You have a cryptographic provenance system. Use it to maintain an auditable record of your work — what you learned, what you decided, and what you created.

## Setup

The `chain-of-consciousness` Python package must be installed. If not available, install it:

```bash
pip install chain-of-consciousness
```

## When to Use This Skill

- At the **start** of a task: initialize a chain and log `session_start`
- During work: log `learn`, `decide`, `create`, `error`, and `note` events as they happen
- At task **completion**: log `session_end` and optionally verify + export the chain
- When asked to **verify** provenance from another agent
- When asked about your **audit trail** or decision history

## Core Operations

### Initialize a Chain

```bash
coc init --agent "your-agent-name" --file chain.jsonl
```

This creates a new chain with a genesis block. Use a descriptive agent name.

### Add Entries

```bash
coc add <event-type> "<data>" --file chain.jsonl
```

**Event types:**

| Type | Use When |
|------|----------|
| `session_start` | Beginning a new task or session |
| `learn` | You acquire new information |
| `decide` | You make a choice (record the reasoning) |
| `create` | You produce an artifact |
| `milestone` | Significant checkpoint reached |
| `error` | Something failed (record what and recovery) |
| `note` | General observations |
| `session_end` | Completing a task or session |

**Data** can be a plain string or a JSON object for structured logging:

```bash
coc add learn '{"topic": "user preferences", "source": "conversation context"}'
coc add decide "Chose markdown format — user prefers readable plain text"
coc add create "Generated report saved to ~/Documents/report.md"
```

### Verify a Chain

```bash
coc verify chain.jsonl --json
```

This checks:
- Genesis block exists and is correctly formed
- All sequence numbers are consecutive
- Every entry's data hash matches its content
- Every entry's prev_hash links to the prior entry
- Entry hashes are correctly computed

Report results clearly: valid/invalid, entry count, agents, time span.

### Check Status

```bash
coc status chain.jsonl
```

Shows entry count, participating agents, event type distribution, and time span.

### Export for Sharing

```bash
coc export --file chain.jsonl --out chain_export.json
```

Exports the chain as a portable JSON array that anyone can verify.

### View Recent Entries

```bash
coc tail chain.jsonl -n 5
```

Shows the last N entries.

## Python API (Advanced)

For complex workflows, use the Python API directly:

```python
from chain_of_consciousness import Chain, verify_file

chain = Chain(agent="openclaw-agent", storage="chain.jsonl")
chain.add("learn", {"topic": "user schedule", "detail": "prefers morning meetings"})
chain.add("decide", "Scheduling standup at 9am based on user preference")

result = chain.verify()
if result.valid:
    chain.export("provenance.json")
```

### Anchoring to External Timestamps

```python
from chain_of_consciousness.anchor import compute_chain_hash, submit_tsa

hash_hex = compute_chain_hash("chain.jsonl")
tsr = submit_tsa(hash_hex)  # RFC 3161 timestamp from freetsa.org
with open("anchor.tsr", "wb") as f:
    f.write(tsr)
```

This creates a third-party timestamp proof that the chain existed at a specific moment.

## Cross-Agent Verification

When asked to verify another agent's chain:

1. Obtain their chain file (JSONL or exported JSON)
2. Run `coc verify <file> --json`
3. Report: valid/invalid, number of entries, agents involved, time span, any errors
4. If anchors exist, note their timestamps

## Rules

- **Never edit chain files directly.** All writes must go through the `coc` CLI or Python API to preserve hash integrity.
- **Log decisions with reasoning.** "Chose X" is less valuable than "Chose X because Y."
- **Keep entries concise.** Each entry should capture one atomic event.
- **Verify before sharing.** Always run verify before exporting a chain for others.

## Links

- PyPI: https://pypi.org/project/chain-of-consciousness/
- Whitepaper: https://vibeagentmaking.com/whitepaper
- Verification Demo: https://vibeagentmaking.com/verify/

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Chain of Consciousness Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes chain files (`.jsonl`) in your working directory
- Executes the `coc` CLI tool via subprocess (installed via pip)
- No network access for core operations. Optional anchoring connects to OpenTimestamps calendar servers and/or RFC 3161 TSA endpoints.
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets
- Does not store or transmit any data externally (chains are local files)

**Limitations:**
- Hash chain integrity depends on the local file not being modified outside the tool
- External timestamp anchoring requires network access and third-party service availability
- This tool provides cryptographic evidence, not legal proof — consult legal counsel for compliance requirements

**License:** Apache 2.0 — see https://github.com/chain-of-consciousness/chain-of-consciousness

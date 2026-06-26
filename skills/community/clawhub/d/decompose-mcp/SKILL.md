---
name: decompose-mcp
description: Decompose any text into classified semantic units — authority, risk, attention, entities. No LLM. Deterministic.
homepage: https://echology.io/decompose
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["python3","python"]},"install":[{"id":"pip","kind":"uv","pkg":"decompose-mcp","bins":["decompose"],"label":"Install decompose-mcp (pip/uv)"}]}}
---

# Decompose

Decompose any text or URL into classified semantic units. Each unit gets authority level, risk category, attention score, entity extraction, and irreducibility flags. No LLM required. Deterministic. Runs locally.

## Setup

### 1. Install

```bash
pip install decompose-mcp
```

### 2. Configure MCP Server

Add to your OpenClaw MCP config:

```json
{
  "mcpServers": {
    "decompose": {
      "command": "python3",
      "args": ["-m", "decompose", "--serve"]
    }
  }
}
```

### 3. Verify

```bash
python3 -m decompose --text "The contractor shall provide all materials per ASTM C150-20."
```

## Available Tools

### `decompose_text`

Decompose any text into classified semantic units.

**Parameters:**
- `text` (required) — The text to decompose
- `compact` (optional, default: false) — Omit zero-value fields for smaller output
- `chunk_size` (optional, default: 2000) — Max characters per unit

**Example prompt:** "Decompose this spec and tell me which sections are mandatory"

**Returns:** JSON with `units` array. Each unit contains:
- `authority` — mandatory, prohibitive, directive, permissive, conditional, informational
- `risk` — safety_critical, security, compliance, financial, contractual, advisory, informational
- `attention` — 0.0 to 10.0 priority score
- `actionable` — whether someone needs to act on this
- `irreducible` — whether content must be preserved verbatim
- `entities` — referenced standards and codes (ASTM, ASCE, IBC, OSHA, etc.)
- `dates` — extracted date references
- `financial` — extracted dollar amounts and percentages
- `heading_path` — document structure hierarchy

### `decompose_url`

Fetch a URL and decompose its content. Handles HTML, Markdown, and plain text.

**Parameters:**
- `url` (required) — URL to fetch and decompose
- `compact` (optional, default: false) — Omit zero-value fields

**Example prompt:** "Decompose https://spec.example.com/transport and show me the security requirements"

## What It Detects

- **Authority levels** — RFC 2119 keywords: "shall" = mandatory, "should" = directive, "may" = permissive
- **Risk categories** — safety-critical, security, compliance, financial, contractual
- **Attention scoring** — authority weight x risk multiplier, 0-10 scale
- **Standards references** — ASTM, ASCE, IBC, OSHA, ACI, AISC, AWS, ISO, EN
- **Financial values** — dollar amounts, percentages, retainage, liquidated damages
- **Dates** — deadlines, milestones, notice periods
- **Irreducibility** — legal mandates, threshold values, formulas that cannot be paraphrased

## Use Cases

- Pre-process documents before sending to your LLM — save 60-80% of context window
- Classify specs, contracts, policies, regulations by obligation level
- Extract standards references and compliance requirements
- Route high-attention content to specialized analysis chains
- Build structured training data from raw documents

## Performance

- ~14ms average per document on Apple Silicon
- 1,000+ chars/ms throughput
- Zero API calls, zero cost, works offline
- Deterministic — same input always produces same output

## Security & Trust

**Text classification is fully local.** The `decompose_text` tool performs all processing in-process with no network I/O. No data leaves your machine.

**URL fetching performs outbound HTTP requests.** The `decompose_url` tool fetches the target URL, which necessarily involves network I/O to the specified host. This is why the skill declares the `network` permission in `claw.json`. If you do not need URL fetching, you can use `decompose_text` exclusively with no network access required.

**SSRF protection.** URL fetching blocks private/internal IP ranges before connecting: `0.0.0.0/8`, `10.0.0.0/8`, `100.64.0.0/10`, `127.0.0.0/8`, `169.254.0.0/16`, `172.16.0.0/12`, `192.168.0.0/16`, `::1/128`, `fc00::/7`, `fe80::/10`. The implementation resolves the hostname via DNS *before* connecting and checks all returned addresses against the blocklist. See [`src/decompose/mcp_server.py` lines 19-49](https://github.com/echology-io/decompose/blob/main/src/decompose/mcp_server.py#L19-L49).

**No API keys or credentials required.** No external services are contacted except when using `decompose_url` to fetch user-specified URLs.

**Source code is fully auditable.** The complete source is published at [github.com/echology-io/decompose](https://github.com/echology-io/decompose). The PyPI package is built from this repo via GitHub Actions ([`publish.yml`](https://github.com/echology-io/decompose/blob/main/.github/workflows/publish.yml)) using PyPI Trusted Publishers (OIDC), so the published artifact is traceable to a specific commit.

## Resources

- [Source Code (GitHub)](https://github.com/echology-io/decompose) — full source, auditable
- [PyPI](https://pypi.org/project/decompose-mcp/) — published via Trusted Publishers
- [Documentation](https://echology.io/decompose)
- [Blog: When Regex Beats an LLM](https://echology.io/blog/regex-beats-llm)
- [Blog: Why Your Agent Needs a Cognitive Primitive](https://echology.io/blog/cognitive-primitive)

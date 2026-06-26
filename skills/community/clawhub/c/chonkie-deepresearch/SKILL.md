---
name: chonkie-deepresearch
description: "Run deep research queries using Chonkie DeepResearch. Returns comprehensive research reports with citations — useful for market analysis, competitive intelligence, technical deep dives, and any research-heavy task."
homepage: https://chonkie.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬",
        "requires": { "bins": ["chdr"] },
        "tags": ["research", "deep-research", "analysis", "reports", "chonkie"]
      }
  }
---

# Chonkie DeepResearch

Run deep research queries from your agent and get comprehensive reports with citations.

## Setup

Before using, check if `chdr` is installed (`which chdr`). If not:

1. Install: `cargo install chdr`
   - If `cargo` isn't available, install Rust first: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. Authenticate: `chdr auth login` (opens browser to get an API key)
   - Or set `CHONKIE_API_KEY` environment variable
   - Get a key at https://labs.chonkie.ai/settings/api-keys

## Usage

**IMPORTANT: Research takes 2-10 minutes. Always spawn a sub-agent to avoid blocking the main thread.**

### Running research (recommended: sub-agent)

Use `sessions_spawn` to run the research in a sub-agent. The sub-agent handles the long-running query and announces the result when done, so your main agent stays responsive.

```json
{
  "tool": "sessions_spawn",
  "task": "Run chdr research and save results. Steps:\n1. Run: chdr research --type report --no-stream --json \"<QUERY>\" > /tmp/chdr-research-<TIMESTAMP>.json\n2. Extract ID and title: python3 -c \"import json; d=json.load(open('/tmp/chdr-research-<TIMESTAMP>.json')); print(d['id']); print(d.get('title','Untitled'))\"\n3. Extract body: python3 -c \"import json; d=json.load(open('/tmp/chdr-research-<TIMESTAMP>.json')); print(d.get('content',{}).get('body',''))\" > /tmp/chdr-research-<TIMESTAMP>.md\n4. Report back the title, ID, and URL: https://labs.chonkie.ai/research/{id}"
}
```

Replace `<QUERY>` with the research query and `<TIMESTAMP>` with `$(date +%s)`.

### Monitoring research status

**Do NOT poll continuously for status.** Instead, set up a cron job to check periodically (every 2-3 minutes):

```bash
# Add a cron entry to check research status every 2 minutes
# The cron should run: chdr view <id> --json | python3 -c "import json,sys; d=json.load(sys.stdin); s=d.get('status','unknown'); print(s)"
# and notify you when status is 'completed' or 'failed'
```

Or simply wait for the sub-agent to announce completion — it will report back automatically when the research finishes. The sub-agent approach is preferred over cron for one-off research queries.

### After research completes

When the sub-agent announces completion:

1. The web URL is: `https://labs.chonkie.ai/research/{id}`
2. The full report is saved at `/tmp/chdr-research-<TIMESTAMP>.md`
3. Read only the first 100 lines for a summary — NEVER load the entire file
4. Tell the user you can answer questions about the report

### Answering follow-up questions

- Grep the `.md` file to find relevant sections before reading
- Use offset/limit to read only the matching section
- NEVER read the entire file into context — reports can be 20,000+ lines

### Fallback: running without sub-agent

If sub-agents are unavailable, run the research command directly but warn the user it will block for several minutes:

```bash
chdr research --type report --no-stream --json "<query>" > /tmp/chdr-research.json
```

### Other commands

```bash
chdr ls                    # List recent research
chdr ls --limit 20         # List more
chdr view <id>             # View a report (supports partial ID prefix)
chdr open <id>             # Open in browser
chdr delete <id>           # Delete a report
```

All commands that take an ID support prefix matching — `chdr view 3a6b` works if unambiguous.

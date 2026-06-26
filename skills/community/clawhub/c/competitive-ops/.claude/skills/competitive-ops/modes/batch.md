# Batch Mode -- Multi-Agent Implementation

**Mode:** `batch`
**Execution:** Parallel multi-agent (one agent per company)

## Overview

Batch mode uses Claude Code's multi-agent capability to analyze multiple competitors **in parallel**. Each company is assigned to a dedicated agent that independently runs the full `analyze` workflow.

**Advantages:**
- ~3x faster for 3 companies (parallel vs serial)
- Independent research per agent (no cross-contamination)
- Scalable to 5+ companies concurrently
- Real-time progress tracking

---

## Workflow

### Step 1: Initialize Batch

1. Parse tier filter from args (e.g., `batch tier 1`)
2. Read `data/batch-queue.md` for company list
3. Filter companies by tier if specified
4. Create team with `TeamCreate`

### Step 2: Create Agent Team

For each company, spawn a dedicated agent:

```
Team: competitive-batch-{timestamp}
├── analyzer-anthropic (analyzes Anthropic)
├── analyzer-openai (analyzes OpenAI)
└── analyzer-google (analyzes Google DeepMind)
```

**Agent Prompt Template:**
```
You are a competitive intelligence analyst agent.

Your task: Analyze the company "{{company}}" using the competitive-ops skill.

Execute the following steps:
1. Run research using web-search, web-fetch, and Tavily MCP
2. Generate SWOT analysis with 6-dimension scoring
3. Create markdown report: data/reports/{date}/{{company}}-{date}.md
4. Update symlink to latest report (always rm first, then ln -s):
   ```bash
   rm -f data/reports/latest/{{company}}.md
   ln -s ../{date}/{{company}}-{date}.md data/reports/latest/{{company}}.md
   ```
   This ensures latest/ always points to the most recent analysis regardless of date.
5. Create snapshot: data/snapshots/{{company}}/{date}.json
6. Update data/competitors.md with new score
7. Generate HTML report using ui-ux-pro-max skill

Output: Final summary with score and report paths.
```

### Step 3: Parallel Execution

All agents execute **concurrently** (max 5 at a time).

### Step 4: Consolidate Results

After all agents complete:
1. Read all snapshots from `data/snapshots/{company}/{date}.json`
2. Update `data/batch-status.json`
3. Generate consolidated report (optional)
4. Output batch summary

---

## Implementation Details

### Team Creation

```javascript
// Pseudo-code for batch execution
const companies = ['Anthropic', 'OpenAI', 'Google DeepMind'];

// Create team
await TeamCreate({
  team_name: `competitive-batch-${Date.now()}`,
  description: 'Parallel competitive analysis'
});

// Spawn agents in parallel
await Promise.all(companies.map(async (company) => {
  await Agent({
    name: `analyzer-${company.toLowerCase().replace(/\s+/g, '-')}`,
    prompt: buildAnalyzePrompt(company),
    team_name: 'competitive-batch-xxx'
  });
}));
```

### Progress Tracking

Track progress in `data/batch-status.json`:

```json
{
  "batch_id": "competitive-batch-xxx",
  "started": "2026-04-07T00:00:00Z",
  "status": "in_progress",
  "agents": [
    { "company": "Anthropic", "status": "running" },
    { "company": "OpenAI", "status": "pending" },
    { "company": "Google DeepMind", "status": "pending" }
  ],
  "total": 3,
  "completed": 0
}
```

### Result Aggregation

After agents complete:

```markdown
## Batch Summary

| Company | Status | Score | Time |
|---------|--------|-------|------|
| Anthropic | ✅ Complete | 79.6 | 45s |
| OpenAI | ✅ Complete | 82.3 | 52s |
| Google DeepMind | ✅ Complete | 82.3 | 48s |

**Total Time:** ~52s (parallel) vs ~145s (serial)
**Reports:** data/reports/{date}/
```

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Agent fails | Mark as "failed", continue others |
| Partial failure | Report failed agents, complete successful ones |
| All fail | Abort batch, output error |

---

## File Outputs

| Type | Location |
|------|----------|
| Batch Status | `data/batch-status.json` |
| Individual Reports | `data/reports/{date}/{company}-{date}.md` |
| Latest Symlinks | `data/reports/latest/{company}.md` |
| Snapshots | `data/snapshots/{company}/{date}.json` |
| HTML Reports | `data/reports/html/{company}-{date}.html` |

---

## Usage

```bash
# Analyze Tier 1 competitors in parallel
/competitive-ops batch tier 1

# Analyze all competitors in batch queue
/competitive-ops batch

# Analyze specific tier
/competitive-ops batch tier 2
```

---

## Example Output

```
🚀 Batch Mode: Multi-Agent Parallel Analysis

Team: competitive-batch-20260407-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Running 3 agents in parallel...

[1/3] 🤖 analyzer-anthropic → Analyzing Anthropic... (running)
[2/3] 🤖 analyzer-openai → Analyzing OpenAI... (running)
[3/3] 🤖 analyzer-google → Analyzing Google DeepMind... (running)

⏱️ Batch started at 00:00:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All agents completed!

| Company | Score | Confidence | Time |
|---------|-------|------------|------|
| OpenAI | 82.3 | 🟢 High | 52s |
| Google DeepMind | 82.3 | 🟢 High | 48s |
| Anthropic | 79.6 | 🟢 High | 45s |

⏱️ Total time: 52s (parallel) | vs 145s (serial)
📁 Reports: data/reports/2026-04-07/
📊 Status: data/batch-status.json
```

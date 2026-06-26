---
name: deep-research-via-gemini-cli-extension
description: "Execute Gemini Deep Research using the gemini-deep-research MCP extension for the Gemini CLI. Use when user wants deep, comprehensive research on a topic — market analysis, industry research, geopolitical analysis, investment research, or any complex multi-source inquiry. Triggers on: deep research X, 帮我研究 X, gemini deep research X, research X thoroughly, 研究一下 X, do a deep search on X, 深度研究 X. Requires: (1) gemini CLI installed (`npm install -g @google/gemini-cli`), (2) gemini-deep-research extension installed, (3) a paid Google AI API key configured via `gemini extensions config gemini-deep-research`. See references/setup-guide.md for setup instructions."
---

# Gemini Deep Research

Executes a full Deep Research workflow via the `gemini-deep-research` MCP extension, with background polling and automatic report saving. The workflow is non-blocking — the agent sets up the task and exits immediately while a background script handles polling.

---

## Prerequisites

See `references/setup-guide.md`. If any prerequisite is missing, inform the user and stop.

---

## Scripts

Three scripts in `<skill>/scripts/`:

| Script | Role |
|--------|------|
| `start-research.js` | Calls `research_start`, outputs JSON with research ID |
| `poll-research.js` | Polls `research_status` every 5 min until done/timeout |
| `save-report.js` | Calls `research_save_report` once status is `completed` |

All scripts read/write `task.json` in the task's temp directory.

---

## Workflow

### Step 1 — Pre-Flight Confirmation (one message, all parameters)

Write in the user's current session language.

```
请确认 Deep Research 参数：

① 研究主题：[用户描述]
   （将原样发给 Gemini，请确保表述清晰具体）

② 报告格式：
   - Comprehensive Research Report（推荐，最全面）
   - Executive Brief（精简版，1-2页）
   - Technical Deep Dive（技术深度分析）

③ 保存位置：~/ObsidianVault/Default/DeepResearch/
   （默认文件名：YYYYMMDD-<slug>.md，可自定义路径）

④ 轮询最大时长：40 分钟（5 分钟 × 8 次），超时后通知您手动处理

直接回复修改项，或"确认"以默认参数启动。
```

### Step 2 — Create Task Temp Directory

```bash
mkdir -p /tmp/gemini-deep-research/<YYMMDD-HHmm>_<sanitized-topic>/
```

Write `task.json`:

```json
{
  "input": "研究主题",
  "format": "Comprehensive Research Report",
  "outputPath": "/home/node/ObsidianVault/Default/DeepResearch/<YYYYMMDD>-<slug>.md",
  "pollIntervalSeconds": 300,
  "maxPolls": 8,
  "createdAt": "<ISO timestamp>"
}
```

### Step 3 — Start Research

```bash
node <skill>/scripts/start-research.js /tmp/gemini-deep-research/<task-dir>/
```

Parse stdout JSON for `{ status: "started", researchId: "v1_..." }`. If `status: "error"`, inform the user and abort.

### Step 4 — Write Background Poll Script

Write `<task-dir>/poll.sh`:

```bash
#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

SKILL_DIR="<skill>/scripts"
TASK_DIR="$(pwd)"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> poll.log; }

log "Starting poll-research..."
node "$SKILL_DIR/poll-research.js" "$TASK_DIR" >> poll-out.log 2>&1
RESULT=$(cat <<< "$(node "$SKILL_DIR/poll-research.js" "$TASK_DIR")")

STATUS=$(echo "$RESULT" | node -pe "JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).status")
log "Poll result: $STATUS"

if [[ "$STATUS" == "completed" ]]; then
  log "Research completed. Saving report..."
  node "$SKILL_DIR/save-report.js" "$TASK_DIR" >> save-out.log 2>&1
  SAVE_STATUS=$(node -pe "JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).status" <<< "$(node "$SKILL_DIR/save-report.js" "$TASK_DIR")")
  log "Save result: $SAVE_STATUS"
  echo "$SAVE_STATUS"
elif [[ "$STATUS" == "timeout" ]]; then
  echo "timeout"
else
  echo "failed"
fi
```

### Step 5 — Launch Background Process

```bash
cd /tmp/gemini-deep-research/<task-dir>/
nohup bash poll.sh > /dev/null 2>&1 &
echo "Background PID: $!"
```

### Step 6 — Notify User

> "🔬 Deep Research 已启动\n\n主题：[topic]\n格式：[format]\n预计完成：2–15 分钟（视主题复杂度而定）\n\n轮询后台运行，完成后我会通知您。如超时（40 分钟）未完成，我会告知并提供手动检查方法。"

### Step 7 — Completion

When the user asks "is it done?" or when notified by a new session:

```bash
# Check done.flag or task.json status
cat /tmp/gemini-deep-research/<task-dir>/task.json
```

**On success:**
> "✅ Deep Research 完成！\n\n主题：[topic]\n报告：[outputPath]\n轮询次数：N\n\n已保存到 ObsidianVault，可在 `DeepResearch/` 目录找到。"

**On timeout:**
> "⏰ Deep Research 超时\n\n主题：[topic]\nResearch ID：`v1_...`\n\n该 ID 在 Google 侧仍可能已完成。可手动保存：\n\`\`\`bash\nnode <skill>/scripts/save-report.js /tmp/gemini-deep-research/<task-dir>/\n\`\`\`\n\n或前往 https://notebooklm.google.com/ 查看。"

**On failure:**
> "❌ Deep Research 失败\n\n原因：[error message]\n\n请检查 API Key 配置（`gemini extensions config gemini-deep-research`）或查询 [references/setup-guide.md](references/setup-guide.md)。"

---

## Report Formats

| Format | Description |
|--------|-------------|
| `Comprehensive Research Report` | Full multi-section report with analysis and citations (default) |
| `Executive Brief` | Condensed summary for decision-makers |
| `Technical Deep Dive` | Detailed technical analysis |

---

## File Naming

Default pattern: `YYYYMMDD-<slug>.md`

- `YYYYMMDD` = today's date
- `<slug>` = lowercase, spaces→hyphens, strip special chars
- Example: `20260325-iran-hormuz-strait-market-impact.md`

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|-----------|
| `API key not found` | Key not configured | Guide to `references/setup-guide.md` step 4 |
| `429 Too Many Requests` | Free-tier key / quota exceeded | Requires paid key |
| Research timed out | Took > 40 min | Check `task.json`, manually save if completed server-side |
| MCP server spawn failed | Extension path wrong | Verify `~/.gemini/extensions/gemini-deep-research/` exists |

---

## Temp Directory Structure

```
/tmp/gemini-deep-research/
  <YYMMDD-HHmm>_<topic>/
    task.json       ← task parameters + research ID
    progress.json    ← poll count, last poll time (updated by poll-research.js)
    poll.log        ← each poll attempt log
    poll-out.log    ← stdout from poll-research.js
    save-out.log    ← stdout from save-report.js
    error.log       ← errors
    done.flag       ← created on success
    <report>.md     ← saved report
```

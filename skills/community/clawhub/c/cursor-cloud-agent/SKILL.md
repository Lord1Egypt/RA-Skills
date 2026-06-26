---
name: cursor-agent
description: >-
  Launch and manage Cursor Cloud Agents via the official API v0.
  Use when user asks to delegate a coding task to Cursor's cloud agent,
  create a PR automatically, or track agent progress.
  Requires python3 and a Cursor API key stored in ~/.cursor_api_key.
---

# Cursor Cloud Agent Skill

Manages Cursor Cloud Agents via the **official API v0** (`api.cursor.com`). Cloud Agents run in isolated cloud VMs, onboard to your codebase, write code, test it, and deliver merge-ready PRs.

## Quick Start

```bash
SKILL=~/.openclaw/workspace/skills/cursor-agent/scripts/cursor_bga.py

# First-time setup: get your API key
python3 $SKILL setup

# Launch an agent and wait for it to finish
python3 $SKILL create \
  --repo owner/repo-name \
  --prompt "Add unit tests for the auth module, run tests, submit PR" \
  --auto-pr --wait

# Launch without waiting (returns immediately)
python3 $SKILL create \
  --repo owner/repo-name \
  --prompt "Refactor utils module" \
  --auto-pr

# List recent agents
python3 $SKILL list

# Check agent details (one-time query)
python3 $SKILL get --agent-id <ID>

# Poll agent until finished (blocks, prints summary when done)
python3 $SKILL check --agent-id <ID> --interval 15 --timeout 600

# Send follow-up instructions
python3 $SKILL followup --agent-id <ID> --message "Also add integration tests"

# Stop a running agent
python3 $SKILL stop --agent-id <ID>

# List available models
python3 $SKILL models

# List accessible repos
python3 $SKILL repos
```

## Authentication

API key is read from (in priority order):
1. `--api-key KEY` argument
2. `CURSOR_API_KEY` environment variable
3. `~/.cursor_api_key` file (recommended)

```bash
# Save API key
echo 'your_api_key_here' > ~/.cursor_api_key
chmod 600 ~/.cursor_api_key
```

Get your key at: **https://cursor.com/dashboard** → Integrations → Generate API Key

## Commands

| Command | Description |
|---------|-------------|
| `create` | Launch a new Cloud Agent (`--wait` to block until done, `--no-direct` to skip auto-execute hint) |
| `list` | List recent agents (filter by PR URL, limit) |
| `get` | Get agent details (status, summary, PR info) |
| `check` | Poll agent until finished, print final summary |
| `conversation` | View full agent conversation history |
| `followup` | Send additional instructions to a running agent |
| `stop` | Pause a running agent |
| `delete` | Permanently remove an agent |
| `models` | List available LLM models |
| `repos` | List accessible GitHub repositories (outputs owner/repo format for `--repo`) |
| `setup` | Print API key setup instructions |

## API Details

- Base URL: `https://api.cursor.com/v0`
- Auth: Basic Authentication (API key as username, empty password)
- Docs: https://cursor.com/docs/cloud-agent/api/endpoints

## Workflow

When user asks to delegate a task to Cursor Cloud Agent:

### Phase 1: Pre-flight Check (automatic)

The `create` command now runs automatic pre-flight checks before launching an agent:

1. **API Key** — Validates key by calling `/models` endpoint
2. **Repo Access** — Verifies the repo is in Cursor's accessible repo list
3. **PR Permissions** (when `--auto-pr`) — Checks GitHub push/admin access via `gh` CLI

If any check fails, the script exits with a clear error message before incurring API costs.

Use `--skip-preflight` to bypass these checks if needed.

You still need to confirm with the user:
- **Task Prompt** — Must be clear and specific enough for an agent to execute independently
- **Branch/Ref** — If user wants changes on a specific branch (not default)

### Phase 2: Execute

5. Run `create --wait --auto-pr` with the confirmed repo and prompt
6. The script auto-appends a "execute directly" instruction to prevent agent from asking for confirmation (use `--no-direct` to disable)
7. `--wait` blocks until agent finishes and prints a full summary including conversation excerpt

### Phase 3: Post-check

8. If `check` reports `--auto-pr` was set but no PR URL, it will print the `gh pr create` command as fallback — run it
9. Use `followup` to refine instructions if agent output needs adjustment
10. Report results back to user

## Agent Status Values

- `CREATING` — Agent is being set up
- `RUNNING` — Agent is actively working
- `FINISHED` — Agent has completed the task
- `FAILED` / `STOPPED` — Agent terminated abnormally

## Constraints

- **Repo 格式** — `--repo` 必须为 `owner/repo` 格式，不支持完整 URL 或纯仓库名
- **Repo 权限** — 只能操作 Cursor GitHub App 已授权的仓库，未授权仓库会返回 404
- **并发限制** — 同一账号同时运行的 Agent 数量受 Cursor 计划限制（Trial 通常为 1 个）
- **执行时长** — 单个 Agent 任务通常在 2-5 分钟完成，复杂任务可能更长；`check` 默认超时 600 秒
- **用量计费** — 每次 `create` 都会产生 API 用量费用，请勿重复创建相同任务
- **Prompt 语言** — Agent 支持中英文 prompt，但代码注释和 commit message 默认跟随 prompt 语言
- **Auto-PR 不保证** — `--auto-pr` 依赖 Cursor GitHub App 权限，可能静默失败（无报错），需在 Post-check 阶段处理

## Troubleshooting

### 1. 认证失败 (401)

```
[ERROR] Authentication failed (401). Check your API key.
```

**原因**：API Key 无效、过期或格式错误

**解决**：
1. 检查 `~/.cursor_api_key` 文件内容是否以 `crsr_` 开头，无多余空格或换行
2. 到 https://cursor.com/dashboard → Integrations 重新生成 Key
3. `python3 $SKILL models` 验证新 Key 是否生效

### 2. 权限不足 (403)

```
[ERROR] Forbidden (403). Your plan may not support this feature.
```

**原因**：当前 Cursor 计划不支持 Cloud Agent API，或未开启 Usage-based pricing

**解决**：到 Cursor Dashboard 确认计划类型，确保已开启 Usage-based pricing

### 3. 仓库未找到 (404)

```
[ERROR] Not found (404): /agents
```

**原因**：仓库名格式错误，或 Cursor GitHub App 未授权该仓库

**解决**：
1. 确认 `--repo` 为 `owner/repo` 格式（如 `siaslfs/ai-xxx`）
2. 到 GitHub → Settings → Applications → Cursor 检查仓库授权

### 4. 请求限流 (429)

```
[ERROR] Rate limited (429). Please wait and try again.
```

**原因**：短时间内请求过多

**解决**：等待 1-2 分钟后重试。避免频繁调用 `create` 或短间隔轮询（`check --interval` 建议 ≥ 10 秒）

### 5. Agent 空转（只输出方案不执行）

**现象**：Agent 状态 FINISHED，但 `filesChanged` 为 0，对话记录显示 Agent 在等待确认

**原因**：Prompt 被 Agent 理解为需要先确认再执行

**解决**：
1. 默认已自动追加"直接执行"指令，正常情况不会发生
2. 如果使用了 `--no-direct`，去掉该参数重试
3. 也可以用 `followup --message "直接执行，不需要确认"` 追加指令

### 6. Auto-PR 未生效

**现象**：Agent FINISHED，有代码变更，但无 PR URL

**原因**：Cursor GitHub App 缺少创建 PR 的权限

**解决**：`check` 会自动输出 `gh pr create` 回退命令，直接执行即可。或到 GitHub 手动创建 PR

## Requirements

- Active Cursor account with Trial or Paid plan
- Usage-based pricing enabled
- GitHub account connected with repository permissions

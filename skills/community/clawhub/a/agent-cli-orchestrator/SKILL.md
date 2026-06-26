# SKILL: agent-cli-orchestrator (Multi AI CLI Orchestrator)

**Version:** 2.0.1 (2026-03-16)  
**Status:** Stable  
**Expertise:** CLI Automation, Error Recovery, Tool Chain Management

---

## ⚠️ 重要：工具检测方式

**必须执行扫描脚本来检测工具**，因为：
- 直接使用 `which` 或 `command -v` 无法获取完整环境变量
- Gemini CLI 等工具安装在用户 shell 配置的路径中
- 必须先 `source ~/.zshrc` 加载环境后再检测

**正确做法：**
```bash
# 1. 先加载环境
source ~/.zshrc

# 2. 再检测工具
command -v gemini
command -v claude
command -v cursor-agent
```

**或使用内置扫描脚本：**
```bash
# 扫描脚本会自动加载环境并检测工具
/Users/atom/.openclaw/workspace/skills/agent-cli-orchestrator/scripts/scan_ai_tools.sh
```

---

## 1. Description

`ai-cli-orchestrator` is a meta-skill that integrates multiple AI CLI tools (such as Gemini CLI, Cursor Agent, Claude Code) to build a highly available automation workflow. It intelligently identifies the AI toolchain in the current environment, allocates the optimal tool based on task type, and achieves seamless task context transfer with automatic fallback when the primary tool encounters rate limits, API failures, or logical bottlenecks.

---

## 2. Trigger Scenarios

- **Complex Coding Tasks:** When large-scale refactoring across files and modules is needed, and a single AI logic hits bottlenecks.
- **High Stability Requirements:** In CI/CD or automation scripts, tasks cannot be interrupted due to single AI service API fluctuations.
- **Domain-Specific Optimization:** Leveraging the strengths of different AIs (e.g., Gemini's long context, Claude's rigorous code logic).
- **Resource Limits:** When the primary tool triggers token or rate limits, need to switch to backup options.

---

## 3. Core Workflow

### 3.1 Discovery Phase

1. **Auto-Scan:** Scan system PATH to detect installed AI CLI tools (`gemini`, `cursor-agent`, `claude`, etc.).
2. **Availability Check:** Run `tool --version` or simple echo tests to verify API key validity.
3. **Environment Sync:** Read `.ai-config.yaml` or `.env` from project root for permission config.

### 3.2 User Configuration

#### 1. Auto-Scan Available AI CLI
```
🤖 AI Assistant Initialization

Detected AI CLI tools:
✅ gemini - Installed
❌ cursor-agent - Not detected
✅ claude - Installed

Select tools to enable (multi-select):
[1] gemini
[2] cursor-agent  
[3] claude
[4] Add custom...
```

#### 2. Add Custom AI CLI
```
Enter command name: kimi
Enter test command: kimi --version
Enter description: Moonshot AI
```

#### 3. Set Priority
```
Priority (lower number = higher priority):
1. gemini
2. claude
```

#### 4. Select Strategy
```
Choose AI response strategy:

[1] AI CLI First
    - When receiving questions, automatically use AI CLI to search for answers first

[2] Direct Response
    - Use model capabilities directly

[3] Hybrid Mode
    - Simple questions answered directly, complex questions use AI CLI
```

### 3.3 Task Dispatching Phase

1. **Intent Recognition:** Analyze user input (Research, Code, or Debug?).
2. **Priority Matching:** Select preferred tool based on priority matrix.
3. **Session Management:** 
   - Check for associated Session ID.
   - For continuous tasks, try to inject intermediate outputs (diff or thought chain) as context to the new tool.

### 3.4 Monitoring & Fallback Phase

1. **Real-time Monitoring:** Monitor CLI stderr and exit codes.
2. **Failure Detection:**
   - Non-zero exit code with "rate limit", "overloaded", "auth error".
   - Output fails local validation 3 times consecutively.
3. **State Handover:** Start backup tool, automatically retry failed instruction.

---

## 4. Configuration Example

Create `.ai-cli-orchestrator.yaml` in project root:

```yaml
version: "2.0"
settings:
  default_strategy: "balanced" # options: speed, quality, economy
  auto_fallback: true
  max_retries: 2

tools:
  gemini:
    priority: 1
    alias: "gemini"
    capabilities: ["long-context", "multimodal", "fast-search"]
  cursor-agent:
    priority: 2
    alias: "cursor"
    capabilities: ["codebase-indexing", "surgical-edit"]
  claude-code:
    priority: 3
    alias: "claude"
    capabilities: ["logic-reasoning", "unit-testing"]

strategies:
  balanced:
    primary: "gemini"
    secondary: "cursor-agent"
    emergency: "claude-code"
```

---

## 5. Error Handling

| Error Type | Detection | Response |
| :--- | :--- | :--- |
| **Rate Limit** | `429 Too Many Requests` | Record offset, switch to next tool, delay 30s then reset. |
| **Logic Loop** | Same File Edit 3 times | Force interrupt, output context, request higher-level tool. |
| **Auth Failed** | `401 Unauthorized` | Try local backup `.env`; if failed, skip and notify user. |
| **Network Timeout** | `ETIMEDOUT` | Retry once; if still fails, switch to offline mode or backup CLI. |
| **Command Not Found** | `command not found` | Skip this tool, switch to next available tool. |
| **Stalled > 30s** | Timeout | Force interrupt, switch tool and retry. |

---

## 6. Session Management

### 6.1 Task Metadata

Each task associates:
- TaskID (unique identifier)
- File snapshots (task-related files)
- Command history (executed commands)
- Last summary

### 6.2 Session Switching Rules

| Scenario | Action |
|----------|--------|
| Same task | Keep long conversation, don't create new session |
| Different task | Create new session |
| Return to previous task | Switch to corresponding session |

### 6.3 Context Recovery

When switching back to old task:
1. Read task summary
2. Load key history fragments
3. Quickly restore state

---

## 7. AI CLI Priority

| Priority | Tool | Purpose | Fallback |
|----------|------|---------|----------|
| 1 | gemini | Primary Q&A/Search | Auto-switch to 2 |
| 2 | cursor-agent | Code tasks | Auto-switch to 3 |
| 3 | claude-code | Emergency fallback | Error and notify user |

---

## 8. Best Practices

- **Atomic Operations:** Execute single-intent tasks to accurately transfer "last successful state" during fallback.
- **Shared Context:** When switching tools, always pass `git diff` or latest `summary.md` to the接管 tool.
- **Protect Credentials:** Never leak API Keys from environment variables in logs or AI prompts.
- **Verification is King:** Always verify with local tools like `npm test` or `ruff` regardless of which AI tool is used.
- **Regular Maintenance:** Run updates monthly to sync the latest versions of all CLI tools.

---

## 9. Available Commands

- `ai-cli-orchestrator init`: Interactive configuration of toolchain and priority.
- `ai-cli-orchestrator run "<task>"`: Execute task based on strategy and manage lifecycle.
- `ai-cli-orchestrator status`: View availability report of all AI services.
- `ai-cli-orchestrator session switch <id>`: Manually migrate data between different AI sessions.

---

## 10. Extensibility

Support integrating new AI CLIs by writing simple adapters. Just provide:

1. `detect()`: How to find the tool.
2. `execute(prompt, context)`: How to call and get output.
3. `parse_error()`: How to parse its unique error types.

---

## 12. Security & Credentials

### Why We Need to Read Config Files

This skill requires reading shell and project configuration files to:
- Scan for installed AI CLI tools in PATH
- Verify API keys/credentials are valid
- Read project-specific AI configs (`.ai-config.yaml`, `.env`)

### Credential Protection

- **Local Processing Only**: All credential checks happen locally on your machine
- **No Data Exfiltration**: Credentials are never sent to external servers
- **Minimal Access**: Only reads necessary config files, never writes or modifies them
- **Sandboxed Execution**: AI CLI tools run in isolated processes

### Best Practices

- Always verify which AI CLIs have access to your credentials
- Use environment-specific API keys (dev vs production)
- Regularly audit installed AI CLI tools

---

## 11. Version History

- v2.0.0 (2026-03-16) - Major update: initialization config, execution strategy, session management, automatic fallback

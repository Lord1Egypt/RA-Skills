# 本机 Coding Agent 调度能力

## 可调度的 CLI Coding Agents

以下工具可从 Hermes 通过 `terminal()` 调用，pipe prompt 并取回结果：

| 工具 | 调度命令 | 状态 | 备注 |
|------|---------|------|------|
| **Claude Code** | `claude -p "prompt" --max-turns N` | ✅ 就绪 | 认证用 `ANTHROPIC_AUTH_TOKEN` 或 OAuth。print mode 最简洁 |
| **OpenAI Codex** | `codex exec "prompt"` (需 pty) | ⚠️ 认证 | `codex login` 需先完成。interactive TUI 需 pty=true |
| **OpenCode** | `opencode run "prompt"` | ⚠️ 认证 | `opencode auth login` 配置 provider |
| **Antigravity CLI `agy`** | `agy -p "prompt"` | ❌ OAuth 锁 | v1.0.7 有 `--print` 模式，但认证仅 OAuth→Windows Credential Manager。Hermes 进程无法访问。GitHub issue #78 请求 API Key 支持 |

## 不可调度的 GUI IDE

以下工具虽是 AI IDE，但无 pipeable CLI 模式，只能控制窗口行为（打开文件/跳转行号/开聊天窗）：

| 工具 | 窗口控制 | 限制 |
|------|---------|------|
| **Cursor** v3.5.8 | `cursor --goto file:line`, `cursor --chat` | 无 `-p` 模式，AI 交互在 GUI |
| **Antigravity IDE** v1.107.0 | `antigravity --goto file:line`, `antigravity chat "p" -m agent` | `chat` 模式打开 GUI 窗，不返回 stdout |

## 安装参考

### Antigravity CLI (`agy`)
```powershell
# Windows
irm https://antigravity.google/cli/install.ps1 | iex
# 安装到 %LOCALAPPDATA%\agy\bin\agy.exe
```
首次运行需在真实终端中完成 OAuth 登录（浏览器跳转），之后凭据存 Windows Credential Manager。

### Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```

### Codex
```bash
npm install -g @openai/codex
```

### OpenCode
```bash
npm install -g opencode-ai@latest
```

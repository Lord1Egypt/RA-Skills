# Claude Code Bridge 使用手册

## 快速开始

| 用户说 | 效果 |
|--------|------|
| `启动cc` | 启动 Claude Code（会询问工作目录） |
| `在 ~/projects/paper 打开cc` | 在指定目录启动 |
| `沙盒打开cc` | 沙盒模式启动（临时目录，关闭自动清理） |
| `关闭cc` / `退出cc` | 关闭会话（沙盒自动清理） |
| `重启cc` | 重启 Claude Code 会话 |
| `cc状态` | 查看当前会话是否活跃 |
| `cc在哪` / `cc目录` | 查看当前工作目录 |
| `/cc peek` | 查看 CC 终端原始画面 |
| `/cc history 100` | 查看最近 100 行对话历史 |
| 其他任何消息（CC 模式中）| 直接转发给 Claude Code |

## 工作目录

启动时可以指定 Claude Code 的工作目录：

- **指定路径**：`在 ~/Documents/Code 打开cc` — CC 在该目录启动，读取该目录的文件和配置
- **沙盒模式**：`沙盒打开cc` — 在 `/tmp/cc-sandbox-xxx` 临时目录启动，关闭时自动清理
- **不指定**：`启动cc` — 会简短询问工作目录，不回复则默认沙盒模式

## CC 斜杠命令

CC 模式下，CC 自身的斜杠命令直接透传：

| 命令 | 作用 |
|------|------|
| `/plan` | 切换到 Plan 模式 |
| `/model sonnet` | 切换模型 |
| `/compact` | 压缩上下文 |
| `/cost` | 查看 Token 用量 |
| `/help` | 查看帮助 |
| `/clear` | 清空上下文 |

## 审批操作

当 CC 需要审批时（执行命令、读写文件等），会出现选择菜单：

```
Do you want to proceed?
❯ 1. Yes
  2. Yes, allow from this project
  3. No
```

直接回复：
- `y` / `是` / `好` / `1` → 同意
- `2` / `一直允许` → 允许该项目
- `n` / `否` / `3` → 拒绝
- `取消` / `cancel` → 取消

## 长任务处理

发送大任务时（如"重构整个项目"），bridge 会自动等待最多 5 分钟。
如果还没完成，会提示你可以发 `/cc peek` 查看进度。

## 典型对话示例

```
用户: 在 ~/projects/paper 打开cc

✅ Claude Code 已启动
📁 工作目录: /Users/you/projects/paper

---

用户: 帮我看看当前目录有什么文件

Bash(ls)
⎿ README.md  src/  tests/  main.tex
项目包含 4 个主要文件/目录...

---

CC 需要审批:
  Do you want to proceed?
  1. Yes  2. Yes, allow from this project  3. No

用户: 1

[执行结果...]

---

用户: /plan

[切换到 Plan 模式]

---

用户: cc在哪

📁 /Users/you/projects/paper

---

用户: 关闭cc

✅ Claude Code 会话已关闭
```

### 沙盒模式示例

```
用户: 沙盒打开cc

✅ Claude Code 已启动
📁 工作目录: /tmp/cc-sandbox-abc123
🧪 沙盒模式（关闭时自动清理）

---

用户: 帮我写个测试脚本

[CC 在沙盒中创建文件...]

---

用户: 关闭cc

🧹 沙盒已清理: /tmp/cc-sandbox-abc123
✅ Claude Code 会话已关闭
```

## 技术细节

- CC 进程运行在 tmux 会话中（名称: `ccb_<session_id>`）
- tmux 滚动缓冲区设为 50000 行，长会话不丢内容
- 输出检测：日志文件大小连续 3 次稳定（每次间隔 0.8s）即视为完成
- 新内容获取：基于 `tmux capture-pane -S -`（全缓冲区）的行号偏移 diff
- 默认超时 90 秒，长任务 `--long` 模式 300 秒
- 审批操作使用 tmux 方向键模拟 TUI 选择（非文本输入）
- 工作目录和沙盒状态存储在 `~/.openclaw/claude-code-bridge/` 下

## 常见问题

**Q: CC 需要审批工具调用时怎么办？**
A: Bridge 会检测审批状态，把选项发给你。直接回复 1/2/3 或 y/n 即可。

**Q: CC 的回复太长怎么办？**
A: 超过 3000 字符会自动截取尾部。发 `/cc history 500` 查看完整历史。

**Q: 会话意外断开怎么办？**
A: 发送 `重启cc` 重新启动。

**Q: 可以同时开多个 CC 会话吗？**
A: 每个 OpenClaw 对话（QQ 私聊/群/Telegram）各自独立，互不影响。

**Q: CC 模式下能用 OpenClaw 的其他功能吗？**
A: 不能，CC 模式下所有消息都转发给 CC。发 `关闭cc` 退出后恢复正常模式。

**Q: 怎么切换 CC 的模型或 Plan 模式？**
A: 直接发 CC 的斜杠命令如 `/model sonnet`、`/plan` 即可，会原样透传给 CC。

**Q: 沙盒模式的文件关闭后还在吗？**
A: 不在。沙盒目录在 `关闭cc` 时自动删除。如需保留文件，关闭前让 CC 复制到其他位置。

# agent-interrupt: AGENTS.md 集成规则

将以下内容添加到你的 agent 的 `AGENTS.md` 中，即可支持精准 kill。

---

## 长任务协议（agent-interrupt 集成）

**在运行任何超过 10 秒的 exec 任务之前���必须先登记进程 PID。**

### 推荐写法（一行式 wrapper）

用 `run.py` wrapper 自动处理登记和清除���无需手动管理：

```bash
python -X utf8 <SKILL_PATH>/scripts/run.py --agent <YOUR_AGENT_ID> -- python your_script.py
```

### 手动登记方式

```bash
# 1. 登记 PID
python -X utf8 <SKILL_PATH>/scripts/mark.py --agent <YOUR_AGENT_ID> --pid <PID> --session <SESSION_ID>

# 2. 运行实际任务
python -X utf8 your_script.py

# 3. 任务结束后清除登记
python -X utf8 <SKILL_PATH>/scripts/mark.py --agent <YOUR_AGENT_ID> --clear
```

### 规则

- 所有预计运行超过 10 秒的脚本，必须通过 `run.py` 启动
- 任务异常退出时，`run.py` 会自动清除登记
- 不要在没有登记的情况下运行长任务

---

## 示例���my_agent 的集成写法

```markdown
## 长任务协议
所有运行超过10秒的脚本，使用 run.py 启动：

python -X utf8 <SKILL_PATH>/scripts/run.py --agent my_agent -- python your_script.py

任务结束后自动清除登记���无需手动操作。
```

---

## SKILL_PATH 说明

`<SKILL_PATH>` 是 agent-interrupt skill 的安装路���，通常为：
- Windows: `C:\Users\<USER>\.openclaw\workspace\skills\agent-interrupt`
- Linux/macOS: `~/.openclaw/workspace/skills/agent-interrupt`

安装后 `install.py` 会自动填入正确路径，无需手动替换。

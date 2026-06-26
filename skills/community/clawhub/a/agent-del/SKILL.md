---
name: agent-del
description: "按照 OpenClaw 官方规范删除一个或多个 agent（代理），自动完成列表展示、确认、执行删除、移到回收站及历史记录。"
metadata:
  openclaw:
    emoji: 🗑️
    requires:
      bins:
        - openclaw
---

# Agent Del — 删除 OpenClaw Agent

按照 OpenClaw 官方规范删除一个或多个 agent，使用 `openclaw agents delete` CLI 命令，自动将数据移到技能目录下的回收站（`{skillDir}/.trash/`），并在 history.md 中记录删除时间和回收站路径。

---

## ⚠️ Agent 必读：防跳步规则（最高优先级）

本技能是**严格五步流程**。未完成当前步的「完成标志」，**禁止**进入下一步。

| 规则 | 说明 |
|------|------|
| **一步一停** | 每步做完、等用户回复（如需），再进入下一步 |
| **第四步只 exec 一次** | 用户确认后，**只执行下面「第四步」里那一条 bash 命令**，不要拆成多条试探 |
| **禁止猜路径** | 不要用 `ls scripts/`、不要假设 `{baseDir}`、不要手写 workspace 下的路径 |
| **禁止抢先 delete** | 第四步完成前，**不要**调用 `openclaw agents delete` |
| **禁止脚本失败后擅自手动删** | 脚本非零退出时，先把**完整 stderr/stdout** 给用户看，问是否重试；只有用户同意才走「手动回退」 |
| **禁止跳过确认** | 用户未明确回复「确认」类字样，不得执行删除 |
| **建议新会话** | 对话很长时，建议用户开新会话再跑本技能，避免 SKILL 被上下文淹没 |

### 当前步骤追踪（Agent 必须在回复里维护）

每轮回复开头用一行标明进度，例如：

```
📍 agent-del 进度：第 2 步 / 共 5 步 — 等待你选择要删除的 agent
```

---

## 流程

### 第一步：列出当前所有 agent

**完成标志：** 已向用户展示编号列表，并等待用户选择。

用 `exec` **只执行这一条**：

```bash
openclaw agents list --json
```

解析 JSON，展示列表。**main 也要列出，但标注不可删除**：

```
📋 当前已配置的 Agent：

1. 📜 main（管仲）— ⭐ 默认 agent — 🔒 不可删除
   - 模型: r730xd-vllm/kasimat-fp8
   - Workspace: /data1/.openclaw/workspace

2. 🎓 xiaolaoshi（小老师）
   - 模型: r730xd-vllm/kasimat-fp8
   - Workspace: /data1/.openclaw/workspace-xiaolaoshi

回复编号来选择要删除的 agent，可多个（如 "2,3" 或 "2 3"）。
```

展示：编号、emoji、agent ID、显示名称、模型、workspace。`isDefault: true` 的标注为默认且不可删。

**本步禁止：** 调用 delete、运行任何删除脚本、猜测要删哪个 agent。

---

### 第二步：用户选择要删除的 agent

**完成标志：** 已解析出 agent ID 列表，并进入第三步展示摘要。

等用户回复编号，解析为 agent ID 列表。

> 若用户选了 main：提示「main 是默认 agent，通常保留。确认要删除吗？」并等用户再次确认。

**本步禁止：** 执行删除或脚本。

---

### 第三步：展示待删除信息并等待确认

**完成标志：** 用户已明确回复「确认」「是的」「删吧」等肯定语。

```
🗑️ 即将删除以下 Agent：

1. xiaolaoshi（小老师）🎓
   - Workspace: /data1/.openclaw/workspace-xiaolaoshi
   - Agent 目录: ~/.openclaw/agents/xiaolaoshi/
   - 模型: r730xd-vllm/kasimat-fp8

⚠️ 删除后将：
- 从 openclaw.json 移除 agent 配置
- 将 workspace 和 agent 目录移到技能目录回收站 `{skillDir}/.trash/`
- 在 history.md 记录删除时间和回收站路径

确认删除？回复「确认」即可。
```

**必须等用户确认后再进入第四步。**

**本步禁止：** 任何 `exec` 删除操作。

---

### 第四步：执行删除（核心 — 只允许一条命令）

**完成标志：** 脚本输出里出现全部阶段标记（见下方 checklist），且 exit code 为 0。

用户确认后，用 `exec` **只执行下面这一条**（把 `<agentId>` 换成实际 ID，多个用空格分隔）：

```bash
bash "$(find "$HOME/.openclaw" -maxdepth 5 -path "*/skills/agent-del/scripts/run-del.sh" -print -quit 2>/dev/null)" <agentId1> <agentId2>
```

> **为什么用 `run-del.sh`：** 入口脚本与 `agent-del.sh` 同目录，find 到即可运行，**不需要** `dirname`、`xargs` 或 `ls scripts/`。

#### 第四步 Agent 行为约束

1. **只 exec 一次** — 不要先 `ls`、不要先单独 `openclaw agents delete`
2. **脚本包办一切** — 回收站备份 → delete → 清残留 → 写 history → 验证
3. **完整输出给用户** — 原样展示脚本 stdout（含 checklist）
4. **不要重复 delete** — 脚本内部已调用 `openclaw agents delete`
5. **失败时** — 展示完整输出 + 退出码，问用户「重试脚本 / 走手动回退 / 取消」；**不要**静默改手动流程

#### 成功 checklist（输出里必须全部出现）

```
[1/5] 验证 agent 是否存在
[2/5] 移到回收站
[3/5] 执行删除命令
[3b/5] 清理残留目录
[4/5] 最终验证
[5/5] 删除完成
```

若缺少任一项 → 视为未完成，**不要**进入第五步，按失败流程处理。

---

### 第五步：完成提示

**完成标志：** 已向用户汇报结果。

根据脚本输出告知：

- ✅ 已删除的 agent 名称与 ID
- 回收站路径（来自脚本输出）
- 剩余 agent 列表（脚本末尾 `openclaw agents list`）
- 可选：是否 `openclaw gateway restart`

> history.md 已由脚本写入，**Agent 不要**再手动读写 history，除非走了手动回退。

---

## history.md 记录格式

```markdown
# Agent 删除记录

## xiaolaoshi (🎓)

- **删除时间:** 2026-06-06 01:43:00 CST
- **Agent ID:** xiaolaoshi
- **显示名称:** 小老师
- **原 Workspace:** /data1/.openclaw/workspace-xiaolaoshi
- **原 Agent 目录:** ~/.openclaw/agents/xiaolaoshi
- **回收站 workspace:** {skillDir}/.trash/agent-xiaolaoshi-20260606-014300-workspace
- **回收站 agent dir:** {skillDir}/.trash/agent-xiaolaoshi-20260606-014300-agentdir
```

---

## 手动回退（仅当用户同意且脚本完全失败）

**触发条件：** `run-del.sh` 找不到、或 exit ≠ 0 且用户选择手动回退。

1. `openclaw agents list --json` 获取 workspace 路径
2. 定位技能目录：
   ```bash
   SKILL_DIR=$(find "$HOME/.openclaw" -maxdepth 5 -path "*/skills/agent-del/SKILL.md" -print -quit 2>/dev/null | xargs dirname)
   ```
3. `mkdir -p "$SKILL_DIR/.trash"`
4. `mv <workspace> "$SKILL_DIR/.trash/agent-{id}-$(date +%Y%m%d-%H%M%S)-workspace"`
5. 移整个 agent 外层目录（含 `agent/`、`sessions/`、`models.json`）：
   `mv ~/.openclaw/agents/<id> "$SKILL_DIR/.trash/agent-{id}-$(date +%Y%m%d-%H%M%S)-agentdir"`
6. `openclaw agents delete <id> --force`
7. 在 `$SKILL_DIR/history/history.md` 追加记录
8. 验证：`test ! -d ~/.openclaw/agents/<id>`

---

## Bash 兼容性

脚本兼容 **Bash 3.2**（macOS 默认）。执行时**务必用 `bash`**，不要用 `sh`。

推荐入口（与第四步相同）：

```bash
bash "$(find "$HOME/.openclaw" -maxdepth 5 -path "*/skills/agent-del/scripts/run-del.sh" -print -quit 2>/dev/null)" <agentId>
```

---

## 已知 Bug

`openclaw agents delete` 经 gateway 时有 bug：配置会从 openclaw.json 移除，但 CLI 可能提前 return，导致官方 trash 逻辑未执行。

**Workaround：** 脚本**先 `mv` 到 `{skillDir}/.trash/`**，再 `openclaw agents delete`，最后清理残留目录。

---

## 注意事项

- `main` 可列出，通常保留不删
- 删除后数据在回收站，**可恢复**
- 若 agent 绑定了 channel，需手动检查 `openclaw.json` 的 bindings

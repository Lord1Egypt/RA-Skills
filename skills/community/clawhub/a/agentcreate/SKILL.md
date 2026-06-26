---
name: agentCreate
description: "创建或卸载独立的 OpenClaw Agent，支持独立工作区、可选通道绑定（飞书/微信等）、模型选择。触发词：创建agent、new agent、创建机器人、agent setup、new bot、卸载agent、删除agent、remove agent"
metadata: {"openclaw": {"emoji": "🤖"}}
---

# agentCreate

创建或卸载独立的 OpenClaw Agent。每个 Agent 拥有独立工作区、独立会话、独立模型，与主 Agent 完全隔离。

技术实现细节：
- 创建流程 → 见 [references/create.md](references/create.md)
- 卸载流程 → 见 [references/delete.md](references/delete.md)

所有 CLI 操作必须通过 qclaw-openclaw skill 的 wrapper 脚本执行，禁止直接调用 `openclaw` 命令。

---

## 创建 Agent

**收集信息（按顺序引导，每次只问必要项）：**

1. **Agent ID**（英文，小写字母/数字/连字符，唯一）
2. **通道绑定**（可选）：先运行 `config get channels` 列出已有通道和账号供选择；若新建账号，收集对应凭据；也可跳过不绑定
3. **模型**：运行 `models list` 获取实时列表供用户选择，默认 `qclaw/modelroute`
4. **确认**：展示汇总表，用户确认后再执行

**执行前检查：**
- Agent ID 未被占用（`agents list`）
- 若绑定通道，账号已存在或已新建

详细命令见 [references/create.md](references/create.md)。

---

## 卸载 Agent

1. 列出所有 agent（`agents list` + `agents bindings`）
2. 用户选择目标 agent（禁止选择 `main`）
3. 展示 agent 信息，用户选择卸载模式：
   - **仅取消通道绑定**（保留工作区和账号）
   - **完全卸载**（删除 agent + 工作区 + 通道账号）
4. 完全卸载需用户输入 `yes` 二次确认（不可恢复）

详细命令见 [references/delete.md](references/delete.md)。

---

## 核心约束

- 禁止删除 `main` agent
- 完全卸载时**必须**同步删除通道账号配置，否则消息可能 fallback 到 main agent
- 删除账号配置必须用 Python 直接操作 `openclaw.json`（`gateway config.patch` 只能合并写入，无法删除 key）
- 新增/修改配置通过 `gateway config.patch` 写入，禁止直接编辑配置文件
- 修改配置前先备份当前值，失败时立即回滚

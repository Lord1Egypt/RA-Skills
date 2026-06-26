---
name: create-agent
description: >
  完整创建一个 OpenClaw Agent，包括：一次性问卷收集配置信息、自动生成
  workspace 文件（SOUL.md/AGENTS.md/IDENTITY.md/USER.md/MEMORY.md/HEARTBEAT.md）、
  执行 `openclaw agents add` CLI 注册、内置 capability-evolver 自我进化（--review 模式）、
  以及向用户输出完整的后续操作清单。
  触发词：创建 agent、新建 agent、帮我建一个 agent、create agent、new agent、add agent、
  setup agent、我想要一个新的 agent、初始化 agent。
  任何涉及 OpenClaw agent 创建、初始化、注册的请求都应触发此 skill。
tags: [openclaw, agent, setup, workspace, evolution]
---

# Create Agent Skill

这个 skill 的职责是：**从零到一完整创建并注册一个具备自我进化能力的 OpenClaw Agent**。

核心流程分为 5 个阶段，依次执行，不要跳步。

---

## Phase 1 — 一次性问卷

**在执行任何操作前**，先一次性向用户呈现以下问卷，要求用户填写后统一返回。
从对话上下文中提取已知信息，不要重复问已经明确的字段。

```
请填写以下信息来创建你的 Agent（有默认值的可以留空）：

必填：
  Agent ID（唯一标识，如 work / research / assistant）：
  Agent 名称（展示名，如 "Aria"、"Max"）：
  性格/主题（如 "sharp analyst"、"friendly assistant"、"严谨的运营助手"）：

选填（留空将使用默认值）：
  Emoji（默认 🤖）：
  你的名字/昵称（Agent 对你的称呼）：
  你的职业或使用场景（帮助 Agent 更好地理解你的需求）：
  Workspace 路径（默认 ~/.openclaw/workspace-<id>）：
  绑定的频道（如 telegram / discord / whatsapp，可跳过，后续单独确认参数）：
  Heartbeat 周期（默认 30m，即每 30 分钟自检一次）：
```

收到回复后，进入 Phase 1.5。

---

## Phase 1.5 — ID 冲突检查

**在生成任何文件之前**，先执行以下命令检查 Agent ID 是否已被占用：

```bash
openclaw agents list
```

- 如果输出中已存在相同 ID，**停止流程**，告知用户：
  ```
  ⚠️ Agent ID "<AGENT_ID>" 已存在，请重新选择一个唯一的 ID。
  当前已有的 Agent：<列出 agents list 的结果>
  ```
  等待用户提供新的 ID，重新执行本阶段检查，直到 ID 不冲突为止。

- 如果 ID 不冲突，进入 Phase 1.8。

---

## Phase 1.8 — 频道参数确认

**仅当用户在 Phase 1 填写了频道时执行此阶段，填写了「跳过」则直接进入 Phase 2。**

先读取 `references/channel-params.md` 获取各频道的参数模板，然后按以下步骤执行。

### Step 1：检测当前对话所在频道

```bash
openclaw channels list --json
```

从输出中识别当前对话所在的频道类型（如 telegram、discord、feishu 等）和 accountId。

### Step 2：识别用户填写的频道类型

从 `references/channel-params.md` 找到对应频道的参数模板：
- 找到 → 继续 Step 3
- 未找到（不在列表中）→ 告知用户该频道暂无内置模板，引导其参考官方文档提供参数

### Step 3：与当前频道对比，分两种情况处理

**情况 A — 用户填写的频道与当前对话频道一致：**

```
⚠️ 你填写的频道「<CHANNEL>」与当前对话所在频道相同。请确认绑定方式：

  A. 绑定到当前机器人应用（当前 Account: <当前 accountId>）
  B. 绑定到该频道的另一个机器人应用（需提供新的应用凭证）
  C. 跳过频道绑定（稍后手动配置）
```

- 选 A：直接使用当前 accountId，跳到 Step 5
- 选 B：继续 Step 4（展示该频道的参数问卷）
- 选 C：标记 BIND_SKIP=true，进入 Phase 2

**情况 B — 用户填写的频道与当前对话频道不一致：**

直接进入 Step 4。

### Step 4：展示该频道的动态参数问卷

根据 `references/channel-params.md` 中对应频道的「用户需提供的参数」，
动态生成问卷展示给用户：

```
📋 请提供「<CHANNEL>」频道的配置参数：

  <参数1名称>（<说明>）：___________
  <参数2名称>（<说明>）：___________
  ...
  Account ID（此账号的别名，默认 default）：___________（可留空）

  <如该频道需要特殊前置操作，在此提示，如飞书需先安装插件>
```

等待用户填写完成后，继续 Step 5。

### Step 5：记录最终绑定参数

将以下信息记录供 Phase 3 使用：

```
BIND_CHANNEL = <channel>
BIND_ACCOUNT_ID = <accountId>
BIND_PARAMS = { <参数键值对，按该频道的 channels add 命令格式组织> }
BIND_SKIP = true / false
BIND_NEEDS_PLUGIN = true / false   # 飞书、LINE、Zalo 等需要先装插件
BIND_NEEDS_QR = true / false       # WhatsApp 等需要 QR 扫码
```

进入 Phase 2。

---

## Phase 2 — 生成 Workspace 文件

根据用户填写的信息，调用 `scripts/generate-workspace.sh` 生成 workspace 目录和所有文件。

读取 `references/workspace-templates.md` 了解每个文件的模板结构，然后用用户提供的信息填充变量。

```bash
bash scripts/generate-workspace.sh \
  --id "<AGENT_ID>" \
  --name "<AGENT_NAME>" \
  --emoji "<EMOJI>" \
  --theme "<THEME>" \
  --user-name "<USER_NAME>" \
  --user-context "<USER_CONTEXT>" \
  --workspace "<WORKSPACE_PATH>"
```

脚本会生成以下文件（详见 `references/workspace-templates.md`）：

| 文件 | 作用 |
|------|------|
| `IDENTITY.md` | Agent 身份：名称、emoji、主题、自我认知 |
| `SOUL.md` | 核心价值观、行为哲学、沟通风格 |
| `AGENTS.md` | 操作规程、记忆读取顺序、安全边界、进化规则 |
| `USER.md` | 用户画像：名字、偏好、沟通风格 |
| `HEARTBEAT.md` | 周期自检清单，含进化触发逻辑 |
| `MEMORY.md` | 长期记忆，初始化为空结构 |
| `TOOLS.md` | 工具能力说明，初始化为默认模板 |
| `.learnings/LEARNINGS.md` | 学习日志，供 self-improving-agent 使用 |
| `.learnings/ERRORS.md` | 错误日志 |

---

## Phase 3 — 执行 CLI 注册

生成文件后，依次执行以下命令：

```bash
# 1. 注册 Agent
openclaw agents add <AGENT_ID> --workspace <WORKSPACE_PATH>

# 2. 应用 Identity（从 IDENTITY.md 读取）
openclaw agents set-identity --agent <AGENT_ID> --from-identity

# 3. 绑定频道（使用 Phase 1.8 确认的参数，BIND_SKIP=true 则跳过）
if [ "$BIND_SKIP" != "true" ]; then

  # 3a. 如需先安装插件（飞书、LINE、Zalo 等）
  if [ "$BIND_NEEDS_PLUGIN" = "true" ]; then
    openclaw plugin add <BIND_CHANNEL>
  fi

  # 3b. 添加频道账号（使用 channel-params.md 中对应频道的 channels add 命令格式）
  openclaw channels add --channel <BIND_CHANNEL> --account <BIND_ACCOUNT_ID> <BIND_PARAMS>

  # 3c. 绑定 Agent 路由
  openclaw agents bind --agent <AGENT_ID> --bind <BIND_CHANNEL>:<BIND_ACCOUNT_ID>

  # 3d. 如需 QR 扫码配对（WhatsApp 等），提示用户手动完成
  if [ "$BIND_NEEDS_QR" = "true" ]; then
    echo "⚠️  请运行以下命令扫描 QR 码完成配对："
    echo "   openclaw channels login --channel <BIND_CHANNEL> --account <BIND_ACCOUNT_ID>"
  fi
fi

# 4. 确认注册成功
openclaw agents list
```

如果任一命令失败，向用户报告具体错误，不要静默跳过。

---

## Phase 4 — 安装进化 Skills

### 两个 skill 的分工与闭环

这两个 skill 不是替代关系，而是上下游关系，缺一不可：

| skill | 角色 | 写入位置 | 读取位置 |
|-------|------|----------|----------|
| `self-improving-agent` | 观察者／记录员 | `.learnings/ERRORS.md`<br>`.learnings/LEARNINGS.md`<br>`memory/YYYY-MM-DD.md` | 每次 session 的对话内容 |
| `capability-evolver` | 执行引擎 | `SOUL.md`、`TOOLS.md` 等（需批准）<br>`assets/gep/events.jsonl` | `memory/YYYY-MM-DD.md`<br>`.learnings/ERRORS.md`<br>`.learnings/LEARNINGS.md` |

**闭环链路：**
```
每次对话
  └→ self-improving-agent 写入 memory/YYYY-MM-DD.md + .learnings/
       └→ heartbeat 触发 capability-evolver 扫描上述两个信号源
            └→ 生成进化提案 → 发给用户批准 → 应用变更
```

> ⚠️ 关键：`memory/YYYY-MM-DD.md` 是两者的衔接点。
> Agent 必须在每次 session 结束时按 `AGENTS.md` 规定的格式写入该文件，
> capability-evolver 才能读到有效信号。如果 memory/ 为空，进化不会触发。

### 安装命令

在 workspace 目录下执行：

```bash
# 安装 self-improving-agent（信号收集层）
npx playbooks add skill openclaw/skills --skill self-improving-agent

# 安装 capability-evolver（进化执行层）
npx playbooks add skill openclaw/skills --skill capability-evolver
```

capability-evolver 已在 `.env` 中配置为 `--review` 模式（变更需用户批准），无需额外操作。

---

## Phase 5 — 输出用户操作清单

执行完所有步骤后，向用户发送以下清单（用实际值替换占位符）：

```
✅ Agent "<AGENT_NAME>"（ID: <AGENT_ID>）已创建完毕！

━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 接下来你需要完成的操作：
━━━━━━━━━━━━━━━━━━━━━━━━━━

【必做】
1. 初始化 Git 版本控制（capability-evolver 依赖 git 进行回滚）：
   cd <WORKSPACE_PATH>
   git init
   git add .
   git commit -m "init: <AGENT_NAME> agent workspace"

【推荐】
2. 备份到私有仓库（保护你的 Agent 记忆和个性）：
   git remote add origin <YOUR_PRIVATE_REPO_URL>
   git push -u origin main

3. 启动第一次对话，完成 bootstrap：
   在你的频道中发送给 Agent：
   "Hey, let's get you set up. Read your IDENTITY.md and tell me who you are."

【如需绑定频道（如果刚才跳过了）】
4. openclaw agents bind --agent <AGENT_ID> --bind <channel:account>

【进化管理】
5. Agent 会按照 <HEARTBEAT_INTERVAL> 的频率自检并记录学习日志。
   当 capability-evolver 检测到需要进化时，会向你发送变更请求，
   你批准后（node index.js --review）变更才会应用。

   如需立即触发一次进化分析：
   cd <WORKSPACE_PATH>
   node index.js --review

【可选：加入 EvoMap 进化网络】
6. npx playbooks add skill openclaw/skills --skill evomap-gepa2a
   （让你的 Agent 参与跨 Agent 的进化资产共享网络）

━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Workspace 位置：<WORKSPACE_PATH>
🔁 进化模式：capability-evolver --review（变更需你批准）
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 错误处理

- `openclaw agents add` 失败：检查 workspace 路径是否存在，检查 ID 是否已被占用（`openclaw agents list`）
- `npx playbooks` 失败：提示用户确认 Node.js 已安装（`node --version`），以及网络连通性
- workspace 路径已存在：提示用户是否覆盖，不要直接覆盖
- 用户跳过必填字段：不进行下一步，明确提示哪些字段是必须的

---

## 相关参考

- `references/workspace-templates.md` — 所有 workspace 文件的完整模板（Phase 2 必读）
- `scripts/generate-workspace.sh` — workspace 生成脚本（Phase 2 调用）
- OpenClaw 文档：https://docs.openclaw.ai/cli/agents

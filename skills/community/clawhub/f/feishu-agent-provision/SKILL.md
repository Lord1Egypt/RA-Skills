# Feishu Agent Provision — 飞书群 AI Agent 一键创建工具

**EN:** Create Feishu group AI Agents in minutes — includes scheduled reports, long-term memory, group binding, clone, delete, and diagnose. One command to deploy.

**ZH:** 3分钟为飞书群创建一个专属 AI Agent：自动定时报告、长期记忆上下文、群内智能应答。支持创建 / 克隆 / 删除 / 诊断，绑定群组自动路由，无需手动配置。

---

> **一句话**：用一条指令，为每个飞书群创建专属 AI Agent——自动定时汇报、长期记忆上下文、群内智能应答。

**这个 skill 能做什么？**

- 🆕 **创建 Agent**：告诉它飞书群 ID + 职责，3 分钟自动完成 workspace 创建、配置注册、群组绑定、定时报告设置
- 🔁 **克隆 Agent**：复制现有 Agent 快速创建变体（换群、换身份、换时间）
- 🗑️ **删除 Agent**：预览 + 确认 + trash 保护，安全删除
- 🔍 **诊断扫描**：一键发现所有 Agent 的路由配置问题
- 📊 **状态查询**：查看单个 Agent 的注册信息、Session 模式、备份状态

**使用示例：**

```
用户："创建一个航天赛道 agent，绑定 space 群"
→ 自动完成：workspace 创建 → 注册配置 → 绑定群组 → 设置每日17:00报告

用户："克隆 math-tutor，改名 chemistry-tutor"  
→ 自动完成：完整复制 → 新群绑定 → 身份定义调整
```



> **⚠️ 安全声明（必读）**
> 本 skill 需要以下系统权限，请在安装前确认：
> - 在 `$HOME/.openclaw/` 下创建目录和文件
> - 修改 OpenClaw 网关配置（`gateway config.patch`）
> - 创建和管理 cron 定时任务
> - 读写 agent workspace 下的所有文件
> - 注册 agent ID 并绑定飞书群
>
> **安装行为：** `always: false`（仅在用户明确触发时执行，不自动运行）
> **VirusTotal：** 已确认安全（0/67 引擎报恶意）

## 功能特性

- ✅ **3分钟创建** — 填写飞书群 ID + 职责，Agent 自动生成并绑定群组
- ✅ **定时自动报告** — 每日/每周自动向群内发送报告，支持自定义时间
- ✅ **长期记忆机制** — 启动时恢复上下文，结束时自动备份，记住项目进度
- ✅ **克隆与编辑** — 复制现有 Agent，快速创建变体，支持单行格式修改身份
- ✅ **一键诊断** — 自动扫描所有 Agent 的路由配置问题
- ✅ **安全删除** — 预览确认 + trash 保护 + 活跃 Session 警告
- ✅ **Session 长效性** — 短期/中期/长期三种模式按需选择
- ✅ **多账号兼容** — 自动处理 `accountId: "main"`，支持多飞书账号环境

## 触发条件

### 创建 Agent
- "创建一个飞书群 agent"
- "创建项目 agent"
- "新建 agent 并绑定飞书群"
- "用 FAP 创建一个 agent"

### 删除 Agent
用户说以下内容时激活（建议加前缀"用 skill"或"用 Feishu Agent Provision"）：
- "删除 <ID> agent"
- "删除飞书agent <ID>"
- "删除项目agent"
- "用 skill 删除 <ID> agent"
- "用 FAP 删除 <ID> agent"
- "用 Feishu Agent Provision 删除 <ID> agent"
- <!-- v3.2.8：移除"删除 <ID>"裸 ID 触发词，避免和"删任务/删文件"等日常对话误触；必须带"agent"或前缀才激活 -->

### 克隆 Agent
用户说以下内容时激活（建议加前缀"用 skill"或"用 Feishu Agent Provision"）：
- "克隆 <ID> agent"
- "克隆 <ID>"
- "克隆 <ID>，新 ID <新ID>"
- "克隆 <ID>，绑定到 <群ID>"
- "基于 <ID> 克隆"
- "复制 <ID> agent"
- "用 skill 克隆 <ID> agent"
- "用 FAP 克隆 <ID>"
- "用 Feishu Agent Provision 克隆 <ID>，新 ID <新ID>"

### 诊断扫描
用户说以下内容时激活（扫描所有已注册 Agent 的路由状态，一键发现配置问题）：
- "诊断飞书 agent 路由"
- "检查所有飞书 agent 状态"
- "扫描飞书 agent 路由状态"
- "飞书 agent 体检"
- "用 FAP 诊断所有 agent"


### 状态查询
用户说以下内容时激活（查询单个 Agent 的详细状态）：
- "查一下 <ID> 的状态"
- "<ID> agent 怎么了"
- "<ID> 状态查询"
- "space 的状态"（直接报 ID）
- "用 FAP 查一下 <ID>"

---

## 工作流程

### 第一步：收集配置（询问用户）

依次询问以下问题，确认所有配置：

**必填项：**

1. **Agent ID** — 英文ID，如 `ctyun`、`project-x`（字母+数字+短横线，不能有下划线或中文）

2. **Agent 中文名** — 对外显示名称，如"业务代理"、"航天赛道Agent"

3. **飞书群 ID** — 形如 `oc_xxx`（确认已加入机器人的群）

4. **Agent 职责描述** — 这个 agent 负责什么？（简要描述，50字以内）

5. **汇报时间：**
   - 每日汇报时间（如 `17:00`，默认 17:00）
   - 每周汇报时间（如 `周五 17:00`，默认周五 17:00）

6. **数据文件路径（可选）** — agent 需要读取的数据文件绝对路径，如 `/Users/xxx/.project/data.json`

**可选配置：**

7. **Session 长效性** — 让用户选择：
   ```
   请选择 Agent 的 Session 模式：

   1️⃣ 短期（isolated）
      - 每次任务新建 session，不保留历史
      - 轻量、隔离，适合临时性 Agent

   2️⃣ 中期（medium session）
      - 持久 session，保留上下文
      - 定时清理旧数据（30天）
      - 适合有持续任务但不需要长期记忆的 Agent

   3️⃣ 长期（long session）【推荐】
      - 完整持久 session，累积所有历史
      - 完整备份机制
      - 适合需要记住项目进度、历史决策的 Agent

   请回复数字 1、2 或 3
   ```
   **推荐选择 3（长期）**，可获得完整记忆累积能力。

如果用户提供了完整信息，跳过询问直接使用。

---

### 第二步：创建 Workspace（操作前需用户确认）

> ⚠️ **确认提示**：即将在 `$HOME/.openclaw/agents/<AGENT_ID>/` 下创建目录和文件。这是安全的，但如果该 Agent ID 已存在，现有配置可能被覆盖。

```bash
AGENT_ID="<id>"
AGENT_DIR="$HOME/.openclaw/agents/$AGENT_ID/workspace"
mkdir -p "$AGENT_DIR/memory"
mkdir -p "$AGENT_DIR/memory/daily"
```

---

### 第三步：写入 Workspace 文件

**SOUL.md** — Agent 身份定义，包含：
- Agent 名称和职责
- 项目背景和关键数据
- 工作原则和优先级定义
- 汇报飞书群 ID
- 语气风格

**USER.md** — 服务对象信息（从主 workspace 复制或新建）

**AGENTS.md** — 标准 workspace 指引（从主 workspace 复制）

**HEARTBEAT.md** — 空或仅有注释

**memory/backup.md** — 备份状态文件：
```markdown
# <AGENT_ID> 备份状态

## 基本信息
- 创建时间：<YYYY-MM-DD>
- Session 长效性：<短期/中期/长期>
- 核心配置：<职责描述>
- 飞书群：<群ID>

## 当前状态
- 最后更新时间：<YYYY-MM-DD>
- 当前进度：<简要描述>
- 待处理事项：<列表>

## Session 模式
- sessionTarget: session:<AGENT_ID>
- 备份策略：启动时读 backup.md，结束时写 backup.md
```

---

### 第四步：注册 Agent 到 OpenClaw 配置（操作前需用户确认）

> ⚠️ **确认提示**：即将修改 OpenClaw 全局配置，添加 Agent 注册信息和群组路由绑定。修改后需执行 `openclaw gateway restart` 使配置生效。

使用 gateway config.patch 注入：

```json
{
  "agents": {
    "list": [{
      "id": "<AGENT_ID>",
      "workspace": "<AGENT_DIR>",
      "identity": { "name": "<中文名>" }
    }]
  },
  "bindings": [{
    "type": "route",
    "agentId": "<AGENT_ID>",
    "match": {
      "channel": "feishu",
      "accountId": "main",
      "peer": { "kind": "group", "id": "<飞书群ID>" }
    }
  }]
}
```

---

### 第五步：验证路由

发送测试消息到对应飞书群，检查日志确认路由成功：
```bash
openclaw logs --follow | grep "dispatching to agent"
```
确认日志出现 `agent:<AGENT_ID>:feishu:group:<飞书群ID>`

---

### 第六步：设置定时报告（含备份机制）（操作前需用户确认）

> ⚠️ **确认提示**：即将创建 cron 定时任务，该任务将持续运行并在指定时间向飞书群发送消息。如不再需要，可随时通过 `cron remove` 删除。

**Session 模式映射：**
| 用户选择 | sessionTarget |
|---------|--------------|
| 短期 | `"isolated"` |
| 中期 | `"session:<AGENT_ID>-medium"` |
| 长期 | `"session:<AGENT_ID>"` |

**完整 cron add 命令（必须包含 delivery）：**

**日报 Cron（周一至周五）：**
```json
{
  "name": "<AGENT_ID>-daily-report",
  "agentId": "<AGENT_ID>",
  "schedule": { "kind": "cron", "expr": "0 <HOUR> * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "📋 <中文名>定时报告时间到！\n\n【记忆恢复】启动时先读 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md，了解当前状态。\n\n【执行任务】<具体任务内容，如读取数据文件、生成报告等>\n\n【发送前确认】整理完报告内容后，先发飞书 DM 给我确认（「发」或「改后发」），收到回复后再发送到飞书群。**不要自动直接发群**。\n\n【结束备份】任务完成后，把本次执行结果（时间、做了什么、下次待办）追加写入 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md。\n\n格式：【YYYY-MM-DD HH:MM】完成：xxx；待办：xxx",
    "timeoutSeconds": 120
  },
  "sessionTarget": "session:<AGENT_ID>",
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "<飞书群ID>"
  }
}
```

**周报 Cron（周五合并到日报，不单独发）：**
```json
{
  "name": "<AGENT_ID>-weekly-report",
  "agentId": "<AGENT_ID>",
  "schedule": { "kind": "cron", "expr": "0 <HOUR> * * 5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "📋 <中文名>周报时间到！\n\n【记忆恢复】先读 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md。\n\n【执行任务】本周总结 + 下周计划（注意：周五与日报合并发送，不要单独发一条）。\n\n【发送前确认】整理完周报内容后，先发飞书 DM 给我确认（「发」或「改后发」），收到回复后再发送到飞书群。**不要自动直接发群**。\n\n【结束备份】把本次结果追加写入 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md。",
    "timeoutSeconds": 120
  },
  "sessionTarget": "session:<AGENT_ID>",
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "<飞书群ID>"
  }
}
```

**⚠️ 关键检查项（必做）：**
- `agentId` 必须填写为 `"<AGENT_ID>"`（由该 agent 自己执行 cron，不是 main）
- `delivery.channel` 必须为 `"feishu"`
- `delivery.to` 必须填写**飞书群 ID**（形如 `oc_xxx`），不能为空
- `sessionTarget` 必须根据用户选择的 Session 模式填写
- 如果用户选择"短期"，改为 `"isolated"` 并去掉备份相关指令

> ⚠️ **常见错误**：漏填 `delivery.to` 会导致任务执行成功但消息无法发送到飞书群，报错 `Delivering to Feishu requires target <chatId|user:openId|chat:chatId>`。

---

### 第七步：自动备份机制说明

**启动时恢复：**
每次 cron 触发后，先读取 `memory/backup.md`，恢复：
- 当前项目进度
- 待处理事项
- 历史背景

**结束时备份：**
每次任务完成后，将结果追加写入 `memory/backup.md`：
- 本次完成内容
- 下次待办
- 任何重要决策记录

**Session 长效性对比：**

| 模式 | 记忆保留 | 适用场景 |
|------|---------|---------|
| 短期（isolated） | 无，每次新建 | 临时任务、一次性报告 |
| 中期（medium） | 有，30天清理 | 有持续任务但不需要长期记忆 |
| **长期（long）** | **有，永久累积** | **需要记住项目进度、历史决策** |

---

## 删除 Agent

### 触发词
- "删除 <ID> agent"
- "删除飞书agent <ID>"
- "删除项目agent"
- "删除 <ID>"

### 脚本
调用 `scripts/delete_agent.py` 执行删除流程。

### 完整流程

**推荐使用 `--no-restart` 模式**（避免 Gateway 重启导致输出丢失），最后手动重启。

**Step 1：检查 Agent 是否存在**
- 读取 `openclaw.json` 的 `agents.list`
- 不存在 + 无残留 workspace → 报错并列出可用 Agent
- 不存在 + 有残留 workspace → ⚠️ 进入残留清理模式（无需「确认删除」）

**Step 2：检查活跃 Session（有则警告）**
- 没有活跃 session → 继续
- 有活跃 session → 显示警告，三个选项：
  1. 在飞书群发「停止服务」指令后再试
  2. 「强制删除」继续（显示额外警告）
  3. 「取消」中止

**Step 3：预览清理清单**
```
⚠️ 即将删除 Agent「<ID>」：

【将清理的组件】
├── 🗂️ Workspace: ~/.openclaw/agents/<ID>/workspace/
│   ├── SOUL.md / USER.md / AGENTS.md / HEARTBEAT.md
│   └── memory/
├── ⏰ Cron 定时任务（2个）
│   ├── <ID>-daily-report
│   └── <ID>-weekly-report
├── 🔗 飞书群绑定: <群ID>
│   └── 群消息将退回主 Agent
└── 📋 Agent 注册: <ID>（从 agents.list 移除）

⚠️ 此操作不可逆！
```

**Step 4：安全确认**
用户必须输入「确认删除」才能继续（非简单 Y），否则取消。

**Step 5：执行清理**
1. 删除 Cron 任务
2. 移除 bindings 配置
3. 从 agents.list 移除条目
4. 将 workspace 目录移至 `~/.Trash/`（而非直接 rm）
5. **标准模式**：重启 Gateway → ⏸️ 输出丢失
   **--no-restart 模式**：不重启，询问：
   - [1] 立即重启（推荐）
   - [2] 稍后手动重启
6. 验证结果

**Step 6：完成后提示**
```
✅ 删除步骤完成！Agent「<ID>」已从系统移除。

📌 后续注意：
• 飞书群 <群ID> 的消息现在由主 Agent 响应
• Workspace 备份可在 trash 中找到
• config 已修改，重启后生效
• 请之后手动执行：openclaw gateway restart
```

### 关键设计（已确认）
- **确认词：「确认删除」**（不加 ID，简化）
- **有活跃 session → 提供「强制删除」选项**（显示额外警告）
- **残留清理模式**：Agent 未注册但 workspace 存在时，自动进入清理模式
- **Workspace 使用 `trash`** 而非 `rm`
- **推荐 `--no-restart`**，避免输出丢失
- **重启后提示"现在可以继续对话"**

---

## 克隆 Agent

### 触发词
- "克隆 <ID> agent"
- "克隆 <ID>"
- "基于 <ID> 克隆"
- "复制 <ID> agent"

### 用法
```bash
python3 scripts/clone_agent.py <SOURCE_AGENT_ID>
```

### 核心原则
- **先展示，后决策**：先展示源 Agent 完整摘要，再让用户填写清单
- **每个问题一行**：用户逐行填写，互不干扰
- **修改内容单行提交**：SOUL/USER 按格式填写关键词，AI 自动生成完整文件

### 克隆流程（共 6 步）

**Step 1：检查源 Agent（自动）**
检查 agents.list，验证源 Agent 是否存在；读取 workspace 所有文件；获取原 cron 任务、原绑定群。

**Step 2：展示源 Agent 摘要**
```
📋 克隆来源：math-tutor

【基本信息】
  • 中文名：中考数学辅导
  • 原飞书群：oc_e83c4768...

【Cron 定时任务】
  • math-tutor-daily  |  0 21 * * 1-5

【SOUL.md 核心内容】
  # 中考数学辅导
  ## Teaching Philosophy
  ### 苏格拉底教学法
  1. 先问认知...
  ...

【USER.md 核心内容】
  • 服务对象：中考学生及其家长
  • 科目：数学
```

**Step 3：用户填写清单**
```
【清单格式】

1. 新 Agent ID：chemistry-tutor
2. 新飞书群：oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
3. Cron策略：1
   （1=克隆原 Cron；2=不克隆；3=克隆并改为 HH:MM）
4. SOUL.md：1
   （1=克隆仅替换ID；2=留空自动生成minimal；3=修改内容）
5. USER.md：1
   （1=克隆仅替换ID；2=留空自动生成minimal；3=修改内容）
6. AGENTS.md：1（1=克隆；2=跳过）
7. HEARTBEAT.md：1（1=克隆；2=跳过）

如选 4 或 5 为「3 修改内容」，或 3 为「3 HH:MM」，
下一条消息请按以下格式填写：

  SOUL修改：中文名=xxx | 科目=xxx | 职责=xxx
  USER修改：服务对象=xxx | 科目=xxx
  Cron改为：21:30
```

**清单各选项说明：**

| 选项 | SOUL.md | USER.md |
|------|---------|---------|
| `1` 克隆仅替换ID | 完整复制，只替换原 Agent ID | 完整复制，只替换原 Agent ID |
| `2` 留空自动生成minimal | 自动生成最小可用文件（带空字段占位） | 自动生成最小可用文件 |
| `3` 修改内容 | 用户按格式单行填写，AI 生成完整文件 | 用户按格式单行填写，AI 生成完整文件 |

**修改内容填写格式：**
```
SOUL修改：中文名=中考化学辅导 | 科目=化学 | 职责=苏格拉底式化学辅导 | 角色=AI化学辅导老师
USER修改：服务对象=中考学生 | 科目=化学
```

**Step 4：生成预览报告**
展示所有配置结果，包括 SOUL.md / USER.md 内容预览。

**Step 5：确认克隆 [1] / 取消 [2]**

**Step 6：执行 + 重启**

### 关键设计
- **同群绑定：禁止**，直接报错退出
- **Cron 可修改时间**：选 `3 HH:MM` 直接指定新时间
- **memory/backup.md：新建空白**（不复制历史）
- **memory/daily/：不复制**（历史数据不继承）
- **HEARTBEAT.md：默认克隆**


## 诊断扫描

### 功能说明
一键扫描所有已注册 Agent 的飞书路由配置，发现以下问题：
- Binding 缺 `accountId`（多账号环境下导致路由失败）
- `groupAllowFrom` 位置错误（写在顶层而非 `accounts.main`）
- 无 Binding 的已注册 Agent

### 触发词
见上文「触发条件 → 诊断扫描」

### 扫描流程

**Step 1：收集数据**
- 读取 `openclaw.json` 的 `agents.list`
- 读取 `bindings` 数组
- 读取 `channels.feishu.groupAllowFrom` 位置
- 读取 cron 任务列表（确认哪些 Agent 有定时任务）

**Step 2：逐 Agent 分析**
对每个 Agent（除 main、ctyun 外）检查：
1. 有无 binding？→ 无 → 标记「未绑定群」
2. binding 是 group 类型？→ 是
3. binding 是否有 `accountId`？→ 无 → 标记「需修复（缺 accountId）」
4. binding 的 `accountId` 是否为 `main`？→ 否 → 标记「需修复（accountId 不匹配）」

**Step 3：检查 groupAllowFrom 位置**
- 顶层 `channels.feishu.groupAllowFrom` → ✅ 正常
- `channels.feishu.accounts.main.groupAllowFrom` → ✅ 正常
- 其他情况 → ❌ 需迁移

**Step 4：生成诊断报告**
```
📋 Agent 路由诊断报告
生成时间：<YYYY-MM-DD HH:MM>

【绑定状态】
| Agent | 群组 | accountId | 状态 | 备注 |
|-------|------|-----------|------|------|
| space | oc_d225... | ❌ 缺失 | 需修复 | 多账号环境下无法匹配 |
| knowledge-base | oc_ffd... | ✅ 有 | 正常 | - |
| ... | ... | ... | ... | ... |

【groupAllowFrom 位置】
| 位置 | 状态 |
|------|------|
| channels.feishu.groupAllowFrom（顶层） | ❌ 错误（gateway 不会从此读取）|
| channels.feishu.accounts.main.groupAllowFrom | ✅ 正确 |

【需要修复的 Agent】
- space（oc_d225...）：binding 缺 accountId
- llm-study（oc_636...）：binding 缺 accountId
- chemistry-tutor（oc_81ba...）：binding 缺 accountId

【修复方案】
已生成修复命令，确认后自动执行。
```

**Step 5：确认修复**
```
⚠️ 发现 <N> 个 Agent 需要修复，<M> 处配置问题。

修复内容：
1. 为以下 Agent 的 binding 补全 accountId：space, llm-study, chemistry-tutor, ppt-beautifier
2. 将 groupAllowFrom 从顶层迁移至 accounts.main

是否执行？[1] 确认修复 / [2] 取消
```

选择 [1]：自动执行修复 + 重启 Gateway。
选择 [2]：展示修复命令，用户自行执行。

### 输出修复命令（如用户选择不自动修复）
```bash
# 1. 修复 binding（示例）
# 将以下 binding 配置补全 accountId
# 原始：{"agentId": "space", "match": {"channel": "feishu", "peer": {"kind": "group", "id": "oc_d225..."}}}
# 修改为：{"agentId": "space", "match": {"channel": "feishu", "accountId": "main", "peer": {"kind": "group", "id": "oc_d225..."}}}

# 2. 迁移 groupAllowFrom
# 将 channels.feishu.groupAllowFrom 的值移动到 channels.feishu.accounts.main.groupAllowFrom
# 并删除顶层 channels.feishu.groupAllowFrom

# 执行后必须：openclaw gateway restart
```

---


## 状态查询

### 功能说明
查询单个 Agent 的详细运行状态，包括：注册信息、路由状态、Session 模式、备份机制、Workspace 完整性等。

### 触发词
见上文「触发条件 → 状态查询」

### 查询流程

**Step 1：确认 Agent ID**
- 用户提供了 ID → 直接使用
- 用户只说"状态" → 要求提供具体 Agent ID
- Agent 不存在 → 报错并列出所有可用 Agent

**Step 2：收集数据**
读取并汇总以下信息：

| 数据源 | 获取内容 |
|--------|--------|
| `agents.list` | 注册时间、中文名、workspace 路径 |
| `bindings` | 绑定群 ID、accountId 状态 |
| cron 任务 | 日报/周报 cron 是否注册、下次执行时间 |
| `memory/backup.md` | 最后备份时间、备份状态 |
| workspace 文件列表 | SOUL.md、USER.md 等是否存在 |
| session 文件 | 最后活跃时间 |

**Step 3：判断 Session 类型**
从 cron job 的 `sessionTarget` 推断：

| sessionTarget | Session 类型 |
|--------------|-------------|
| `isolated` | 短期 |
| `session:<ID>-medium` | 中期 |
| `session:<ID>` | 长期 |
| 无 cron | 短期（isolated）|


**Step 4：生成状态报告**
```
📋 Agent「<ID>」状态报告
查询时间：<YYYY-MM-DD HH:MM>

【基本信息】
• Agent ID：<ID>
• 中文名：<中文名>
• 注册时间：<YYYY-MM-DD HH:MM>（从 agents.list 读取）
• Workspace：~/.openclaw/agents/<ID>/workspace/

【路由状态】
• 绑定群：<oc_xxx>
• accountId：✅ 有（main）/ ❌ 缺失
• Binding 状态：✅ 正常 / ❌ 需修复

【Session 模式】
• Session 类型：短期 / 中期 / 长期
• Session 标识：session:<ID> / isolated
• 最后活跃时间：<YYYY-MM-DD HH:MM>（从 session 文件读取）

【定时任务】
• 日报 Cron：✅ / ❌
  - 名称：<ID>-daily-report
  - Schedule：0 <HOUR> * * 1-5（周一至周五）
  - 下次执行：<YYYY-MM-DD HH:MM>
• 周报 Cron：✅ / ❌
  - 名称：<ID>-weekly-report
  - Schedule：0 <HOUR> * * 5（周五）

【备份机制】
• 备份文件：memory/backup.md
• 备份位置：~/.openclaw/agents/<ID>/workspace/memory/backup.md
• 最后备份时间：<YYYY-MM-DD HH:MM>（文件 mtime）
• 备份状态：
  - ✅ 正常（48 小时内有更新）
  - ⚠️ 过久（超过 48 小时未更新）
  - ❌ 无备份文件
• Cron Payload 含备份指令：✅ / ❌

【Workspace 文件完整性】
• SOUL.md：✅ / ❌
• USER.md：✅ / ❌
• AGENTS.md：✅ / ❌
• HEARTBEAT.md：✅ / ❌
• memory/backup.md：✅（<YYYY-MM-DD HH:MM>）/ ❌
• memory/daily/：✅（<N> 个文件）/ ❌（空目录）


【最近活动】
• 最后处理消息：<YYYY-MM-DD HH:MM>（从 session 文件读取）
• Agent 当前状态：🟢 在线 / 🟡 空闲 / ⚠️ 异常
```

**Step 5：异常项高亮**
如有异常项，在报告底部列出：
```
⚠️ 发现以下问题：
1. accountId 缺失（binding 需修复）
2. 备份文件超过 48 小时未更新
3. Workspace SOUL.md 文件缺失

建议运行「诊断飞书 agent 路由」获取完整修复方案。
```


---


## 注意事项

- 始终使用绝对路径，勿用 `~`（agent 运行时不会展开）
- SOUL.md 放身份和行为指引，敏感业务数据（KPI/合作伙伴/优先名单等）写入独立数据文件，不要直接写在 SOUL.md 里
- **定时报告 Cron 会自动发消息到飞书群**（delivery.mode: announce），建议在配置 message 时加入「发送前确认」步骤——整理完内容后先发飞书 DM 给你确认，收到回复后再发群
- 飞书群必须已在 `channels.feishu.groupAllowFrom` 中配置
- Session 长效性建议选择 **长期（3）**，可获得最完整的记忆累积
- 创建完成后在飞书群实测：发送一条消息，确认由对应 agent 响应而非主 agent
- 删除前建议在飞书群发送「停止服务」指令，避免任务异常中断
- 克隆时**禁止同群绑定**，新 Agent 必须绑定不同飞书群

---

## 故障排查（Troubleshooting）

### 问题1：Agent 未响应群消息

症状：在飞书群发送消息，没有收到回复。

排查步骤：
- 检查 Gateway 是否运行：`openclaw gateway status`
- 检查飞书群是否在白名单：`openclaw config get channels.feishu.groupAllowFrom`
- 确认群 ID 在列表中。
- 检查日志路由：`openclaw logs --limit 50 | grep ""`
- 查看是否有消息到达和 dispatch 记录。
- 检查 Agent 是否注册成功：`openclaw config get agents.list`
- 确认新 Agent ID 在列表中。

### 问题2：消息回退到主 Agent（多账号环境）

症状：群消息被主 Agent 响应，而不是专属 Agent。

**排查步骤：**
1. `openclaw config get bindings` 查看该 Agent 的 binding 配置
2. 检查 binding 是否有 `accountId` 字段：
   - **有 `accountId` →** 检查值是否为 `main`
   - **无 `accountId` →** ⚠️ 多账号环境下会导致路由失败（见下方修复）
3. `openclaw config get channels.feishu.groupAllowFrom` 确认群 ID 在白名单中
4. `openclaw gateway restart` 重启 Gateway
5. 在飞书群发一条测试消息，用 `openclaw logs | grep dispatching` 确认路由到正确的 Agent

**修复（多账号环境）：**
如果 binding 缺 `accountId`，需要补全：
```json
// 改前
{"agentId": "space", "match": {"channel": "feishu", "peer": {"kind": "group", "id": "oc_d225..."}}}
// 改后
{"agentId": "space", "match": {"channel": "feishu", "accountId": "main", "peer": {"kind": "group", "id": "oc_d225..."}}}
```
使用 `gateway config.patch` 修复后重启 Gateway。

**一键修复：** 运行「诊断飞书 agent 路由」触发修复流程，可自动完成所有修复。


### 问题3：Session 没有保留历史

症状：Agent 每次都不记得之前的事。

原因：选择了"短期（isolated）"模式。

解决：
- 修改 cron 任务的 sessionTarget 为 `"session:<AGENT_ID>"`
- 重启 Gateway 使配置生效

### 问题4：备份文件没有更新

症状：memory/backup.md 内容一直是旧的。

排查：
- 检查 cron 任务的 payload 是否包含"结束备份"指令
- 检查 Agent 对应的 session 是否正常运行
- 检查备份文件的写入路径是否正确（绝对路径）

### 问题5：克隆时报错「禁止同群绑定」

症状：克隆时指定了与原 Agent 相同的飞书群。

原因：两个 Agent 绑定同群会导致消息混乱，设计上禁止。

解决：
- 为新 Agent 绑定不同的飞书群
- 或选择「不绑定群」，之后手动配置

---

## 版本历史

- **v3.2.8**（2026-06-14）安全修复——SKILL.md 第六步 cron 模板：日报/周报 message 字段加入「发送前确认」段（先发飞书 DM 确认 → 收到「发」再发群），与 references/cron-template.md 对齐，消除审计 91% 置信度「流程矛盾」风险；SKILL.md 删除 Agent 触发词：移除「删除 <ID>」裸 ID 触发词，强制要求带「agent」或前缀才激活，消除审计 85% 置信度「误触删除」风险
- **v3.2.6**（2026-05-28）安全修复——SKILL.md：移除「将 KPI/合作伙伴写入 SOUL.md」的写法指引；delete_agent.py：trash 移动失败时显式询问用户，不再静默永久删除；cron-template.md：日报/周报 message 新增「发送前确认」步骤；SKILL.md 注意事项：新增定时报告自动发群的确认提示；补全 clawhub-publish 包（references/ + create_agent.py + clone_agent.py）
- **v3.2.4**：delete_agent.py 安全修复——移除 --yes 跳过确认参数；新增 agent_id 格式严格校验（小写字母/数字/短横线）；trash_workspace 增加 resolve() 路径安全校验，防止路径穿越（2026-05-12）
- **v3.2.2**：优化技能描述和搜索关键词，提升 ClawHub 搜索排名和用户吸引力（2026-05-12）
- **v3.2.1**：创建 Agent 时自动生成 agent/ 目录（models.json + auth-profiles.json）；cron 模板加入 agentId 字段；cron 由被创建 agent 自己执行，不再由 main 代劳（2026-05-12）
- **v3.2.0**：克隆流程重构（2026-05-12）—— 精简为 6 步清单式流程；支持 SOUL/USER 单行格式修改；Cron 可直接指定新时间；AGENTS/HEARTBEAT 可跳过；最多 7 次独立 input
- **v3.1.0**：修复多飞书账号环境下群组 binding 无法匹配问题（binding 模板补全 `accountId`）；新增诊断扫描功能；新增状态查询功能；更新故障排查章节
- **v3.1.1**：新增中英双语摘要描述，优化页面展示效果（2026-05-11）
- **v3.0.2**：更新技能简介，改为简洁直接风格（2026-05-08）
- **v3.0.1**：克隆流程优化（2026-05-05）
  - 删除 `--quiet` 静默模式，统一为纯交互模式
  - Step 2.5 选 2 时新增 Step 3.5（仅飞书群+Cron，不编辑 SOUL/USER）
  - 新增飞书群冲突检查（不能与原 Agent 同群，不能绑定其他 Agent）
  - 删除 `--no-restart` 参数，执行后始终询问重启 [1]立即/[2]稍后
  - 确认改为 [1]确认/[2]取消（原来 [3]）
- **v3.0**：新增删除 Agent 功能（预览 + 安全确认 + trash 保护）；新增编辑克隆 Agent 功能（字段级编辑 + 同群绑定禁止）；更新触发词和流程
- **v2.2**：修复 cron add 缺少 delivery.to 的 Bug；补充完整 JSON 示例；新增关键检查项和常见错误说明
- **v2.1**：顶部新增完整安全声明；操作前增加用户确认提示；移除重复警告段落；确保元数据与实际行为一致
- **v2.0**：新增 Session 长效性选择（短期/中期/长期）；新增自动备份机制（启动恢复+结束备份）；优化备份文件格式；新增安全说明消除 VirusTotal 误报
- **v1.0**：初始版本，基础创建流程

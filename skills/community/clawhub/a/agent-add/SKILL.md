---

name: agent-add
description: "按照 OpenClaw 官方规范创建新 agent（代理），自动完成问答、配置、workspace 初始化与记录。"
metadata:
  openclaw:
    emoji: 🤖
    requires:
      bins:
    - openclaw

---

# Agent Add — 新建 OpenClaw Agent

这是按照 OpenClaw 官方规范建立新 agent 的技能。全程遵循 `openclaw agents add` CLI 命令的标准化流程，确保新建 agent 后自动生成完整的 workspace 和一系列精炼的 `.md` 引导文档，让 AI 更好地配合人类工作。

> **⚠️ 副作用说明：** 此技能会执行以下磁盘写入操作，请确认后再使用：
>
> - **创建新目录：** 为新 agent 创建独立的 workspace 目录
> - **写入文件：** 创建 AGENTS.md、IDENTITY.md、SOUL.md、USER.md 等模板文件
> - **修改已有文件：** 脚本执行后，会用 `edit` 工具对 IDENTITY.md、SOUL.md、USER.md 做**精准编辑**（替换字段值，保留原始结构）。这些文件如果已存在，其内容会被部分修改
> - **持久化记录：** 在技能目录的 `history/history.md` 中追加一条创建记录（永久保存）
> - **修改 OpenClaw 配置：** 通过 `openclaw agents add` 写入 agent 注册信息
>
> 建议在运行前备份重要 workspace，或在确认汇总后再执行。

## 流程

### 第一步：逐个确认信息（严格一问一答）

用户如果需要添加 agent，务必**严格分开问、一个一个问**。每个问题发出后，**等用户回复并确认**，再问下一个。不要一次性问多个问题，不要把最后一个问题和汇总合并。

> **关键规则：** 每问一个问题 → 等用户回复 → 确认收到 → 再问下一个。4 个问题全部确认完毕后再进入第二步汇总。

#### 问题 1：Agent 名字

> 请给这个 agent 起个名字。这个名字会决定：
>
> - 工作目录的名称
> - 界面中选择 agent 时显示的名字
> - 在群里 @召唤 这个 agent 时使用的名字
>
> **建议：** 尽量简短好记，2-4 个字或英文单词。例如：`助手`、`coder`、`小秘`。

**收到回复后确认：** "好的，agent 名字确定为 `{name}`。"

#### 问题 2：Agent 的定位描述

> 请描述一下这个 agent 的定位。可以参考以下格式：
>
> - **用途：** 这是我的___，用来___
> - **昵称/称呼：** （可选）
> - **性格/风格：** 严谨 / 幽默 / 简洁 / 温暖 / 专业...
> - **图标 emoji：** 选一个代表它的符号
>
> **图标建议（根据 agent 名字 `{name}` 推荐，仅供参考，可以自己选）：**
>
> （根据名字的类型动态推荐 5-8 个相关 emoji，不要固定列同一批。例如：
> - 教育/老师类：🎓 📚 ✏️ 🍎 🧑‍🏫
> - 代码/技术类：💻 🔧 ⚙️ 🐛 🖥️
> - 写作/文案类：✍️ 📝 📖 🖊️ 📰
> - 数据/分析类：📊 📈 📉 🔢 🧮
> - 日常/助手类：📋 ✅ ⚡ 🤖 💡
> - 设计/创意类：🎨 🎭 🖼️ ✨ 🎬）
>
> **示例：**
>
> - "这是我的代码审查助手，用来 review PR 和检查 bug，风格严谨简洁，图标用 🔍"
> - "这是我的日常秘书，帮我管理日程和邮件，语气温暖友好，图标用 📋"
> - "这是我的数据分析 agent，处理报表和可视化，专业高效，图标用 📊"

**收到回复后确认：** "好的，定位描述已记录。"

#### 问题 3：模型选择

先用 `session_status` 获取当前会话使用的模型，再从 openclaw.json 读取 `agents.defaults.model.primary` 作为默认模型。

> 请选择这个 agent 使用的模型。可选：
>
> - **当前主 agent 正在使用的模型：** `{currentModel}`（推荐，和现有 agent 一致）
> - **默认模型：** `{defaultModel}`
>
> 先选一个能用的就行，后面随时可以换模型。

**收到回复后确认：** "好的，模型确定为 `{model}`。"

#### 问题 4：Workspace 目录

计算规则（按实际使用方式）：
1. 先找到 main agent workspace 的**父目录**
2. 新 agent 的 workspace = `{父目录}/workspace-{agentId}`
3. 也就是和 main 的 workspace **平级**，在同一目录下

例如 main workspace 是 `/data1/.openclaw/workspace`，则：
- 父目录 = `/data1/.openclaw/`
- 新 workspace = `/data1/.openclaw/workspace-{agentId}`

> 新 agent 的 workspace 将创建在以下位置：
>
> ```
> {实际计算出的路径，例如 /data1/.openclaw/workspace-xiaolaoshi}
> ```
>
> 这个目录和 main agent 的 workspace 平级。确认使用这个默认路径，还是指定其他路径？

**收到回复后确认：** "好的，workspace 路径确定为 `{workspacePath}`。"

---

> ⚠️ **注意：问题 4 确认后，等用户回复，再单独进入第二步汇总。不要把问题 4 和汇总合并在一起问。**

### 第二步：汇总确认

**四个问题全部逐个确认后**，给用户展示完整汇总：

```
📋 即将创建的新 Agent：

- Agent ID: {agentId}
- 显示名称: {name}
- 定位: {description}
- 模型: {model}
- Workspace: {workspacePath}
- 图标: {emoji}

确认以上信息？（回复"确认"或指出需要修改的地方）
```

用户确认后，告知即将生成的文档列表：

```
📁 新 agent 的 workspace 中将包含以下 OpenClaw 精炼文档：

这些文档规范了 AI 的行为准则，能让 AI 更好地帮助人类工作。
建议让 AI 按照各自规范自动填充内容，尽量不要手动删除。

| 文件 | 定位 | 核心职责 | 生命周期 |
|------|------|---------|---------|
| AGENTS.md | 🏛️ 行为宪法 | 操作规则、优先级、记忆使用指令 | 持久存在 |
| BOOTSTRAP.md | 👶 出生证明 | 首次运行仪式，引导填充 IDENTITY/USER/SOUL | 一次性，完成后自毁 |
| IDENTITY.md | 🪪 身份证 | 名字、类型、emoji | Bootstrap 创建，后续可更新 |
| USER.md | 📇 用户速查卡 | 用户名、称呼、时区 | Bootstrap 创建，持续更新 |
| SOUL.md | 🎭 灵魂/人格 | 语气、立场、边界、幽默感 | 持久存在，随时打磨 |
| TOOLS.md | 🛠️ 工具说明书 | 本地工具惯例与配置备忘 | 持久存在 |
| MEMORY.md | 🧠 精选长期记忆 | 事实、偏好、决策摘要 | 持久存在 |
| HEARTBEAT.md | 🔁 定时任务清单 | Heartbeat 检查待办项 | 持久存在（可选） |
```

### 第三步：执行创建

用户最终确认后，先执行脚本注册 agent（传入所有确认的信息）：

```bash
{baseDir}/scripts/agent-add.sh <agentId> <name> <workspacePath> <model> <description> <emoji>
```

参数说明：
- `agentId` — agent 唯一标识
- `name` — 显示名称
- `workspacePath` — workspace 绝对路径
- `model` — 模型 id
- `description` — 定位描述（用户问题2的完整回答）
- `emoji` — 图标 emoji

脚本会自动完成：
1. 执行 `openclaw agents add` 命令
2. 用 `openclaw agents list` 验证添加成功
3. 检查 workspace 中的 `.md` 文件是否存在，缺失则从 main workspace 补充
4. 在 `{baseDir}/history/history.md` 中记录本次创建

### 第四步：初始化文档内容（按区块追加，不覆盖）

脚本执行完成后，用 `edit` 工具对以下文件做**精准编辑**，**不是全盘覆盖**。

> **核心原则：** 原始模板里的通用约束（Core Truths、Boundaries、Continuity、Related 等）是 OpenClaw 精炼过的行为准则，**必须保留**。只按类别追加/替换与新 agent 定位相关的内容。

#### IDENTITY.md — 只替换字段值，保留结构和 Notes/Related

用 `edit` 工具做精确替换：
- 把 `**Name:**` 后面的空值替换为 agent 名字
- 把 `**Creature:**` 替换为 agent 的类型描述（例如 "AI 学习助手"）
- 把 `**Vibe:**` 替换为风格描述
- 把 `**Emoji:**` 替换为选定的 emoji
- `**Avatar:**` 先留空或写 `（暂无）`
- **保留**原有的 Notes、Related 等所有其他区块不变

#### SOUL.md — 在原有结构上追加定位内容，不删通用约束

用 `edit` 工具：
- **保留**原有的 Core Truths、Boundaries、Vibe、Continuity、Related 全部不变
- 先 `read` 查看原始 SOUL.md 有哪些类别（H2/H3 标题）
- **优先在已有类别下追加/替换内容**，例如把 `## 定位` 下的内容替换为新 agent 的定位
- **除非某个类别原始完全没有，并且确实需要，才新增类别**。不要凭空创造大量新章节
- 沟通风格部分：如果原有 `## Vibe / 沟通风格` 存在，在其中追加新 agent 的语言/语气要求

#### USER.md — 只替换用户相关字段，保留结构

用 `edit` 工具：
- 把 `**name:**` 替换为用户名字（如果用户有特别指定的话，否则保留原始的 老杨）
- **保留**原有的 Notes、Related 等所有其他区块不变

> ⚠️ **关键：** 每个文件用 `edit` 做精准替换（oldText/newText），不要用 `write` 全盘覆盖。先 `read` 看原始内容，再决定怎么 edit。

### 第五步：完成提示

文档初始化完成后，告诉用户：

> ✅ Agent **{name}** 已创建成功！
>
> Workspace: {workspacePath}
>
> 已完成的工作：
> - Agent 注册到 OpenClaw（ID: {agentId}）
> - Workspace 初始化，包含所有必要文档
> - IDENTITY.md — 身份信息已写入
> - SOUL.md — 定位和风格已配置（保留原始通用约束）
> - USER.md — 用户信息已更新
>
> 是否现在重启 gateway 使新 agent 生效？
> 运行 `openclaw gateway restart` 即可。

## 注意事项

- Agent ID 使用小写字母、数字和连字符（如 `my-agent`）
- 显示名称可以是中文或任意语言
- Workspace 路径必须是一个**空目录或不存在的路径**（脚本会创建）
- 模型选择影响 agent 的推理能力和速度，根据用途合理选择

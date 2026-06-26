---
name: auto-create-skill
description: >
  从会话中识别固定工作流并自动生成可复用的 Skill。用户下次只需提供关键参数即可
  重复执行相同流程。同时支持对已创建的 Skill 进行增量更新（添加步骤、修改流程、
  删除步骤、调整顺序等）。

  当用户提到以下任意情况时，立即使用本 Skill：
  - "把这个流程保存为 skill" / "把这个工作流抽取出来"
  - "创建一个自动化流程" / "我想把这个固定下来"
  - "帮我生成一个 skill 来做 XXX"
  - "更新/修改/编辑 XXX skill" （其中 XXX 是由本 skill 创建的）
  - "给 XXX 流程加一个步骤" / "删掉 XXX 流程里的某步"
  - "列出我创建的所有 skill" / "查看 skill 列表"
  - 用户描述了一个重复性工作流并暗示想自动化
  - 用户在会话中反复执行类似操作并表示想固化流程
---

# Auto Create Skill

本 Skill 的核心能力：**从对话中提取可复用的工作流，生成结构化的 Skill 文件，
让 Claude 在后续会话中能按照固定流程执行任务。**

---

## 核心概念

### 什么是「工作流 Skill」

工作流 Skill 是一个结构化的 SKILL.md 文件，它定义了：
1. **触发条件**：什么场景下应该使用这个流程
2. **输入参数**：用户需要提供哪些信息（如 Jira ID、分支名等）
3. **执行步骤**：按顺序排列的操作步骤，每步包含：具体动作、使用的工具/MCP、
   是否需要用户确认、失败时的处理方式
4. **流程控制**：条件分支、循环、用户交互点

### 环境检测（关键！）

在创建或更新 Skill 之前，必须先检测当前运行环境，因为不同环境的 Skill
安装路径完全不同。执行以下检测逻辑：

```bash
# 环境检测
if [ -d "$HOME/.claude" ] && command -v claude &>/dev/null; then
  echo "ENV=claude-code"
  echo "SKILL_DIR=$HOME/.claude/skills"
  echo "REGISTRY=$HOME/.claude/skills/.auto-skill-registry.json"
elif [ -d "/mnt/skills/user" ]; then
  echo "ENV=claude-ai"
  echo "SKILL_DIR=/mnt/user-data/outputs"
  echo "REGISTRY=/mnt/skills/user/.auto-skill-registry.json"
else
  echo "ENV=unknown"
  echo "SKILL_DIR=$HOME/.claude/skills"
  echo "REGISTRY=$HOME/.claude/skills/.auto-skill-registry.json"
fi
```

各环境的行为差异：

| 环境 | Skill 写入路径 | 安装方式 |
|------|---------------|---------|
| **Claude Code** | `~/.claude/skills/<skill-name>/` | 直接写入，立即生效，下次会话可通过 `/skill` 调用 |
| **Claude.ai** | `/mnt/user-data/outputs/<skill-name>/` | 生成文件供用户下载，用户需到 Customize > Skills 手动上传 |
| **未知环境** | `~/.claude/skills/<skill-name>/` | 尝试直接写入，失败则输出到当前目录 |

**Claude.ai 特别注意**：Claude.ai 的代码执行环境是临时沙箱，写入
`/mnt/skills/user/` 的文件在会话结束后会消失。所以必须：
1. 将生成的 Skill 文件输出到 `/mnt/user-data/outputs/` 供用户下载
2. 使用 `present_files` 工具向用户展示文件下载链接
3. 明确告知用户：「请下载此文件，然后到 Customize > Skills 上传安装」

### 工作流 Skill 的目录结构（严格遵守！）

Claude Code 的 Skill 加载机制要求：**文件必须放在以 skill 名称命名的子目录下，
文件名必须是 `SKILL.md`（全大写）**。这不是建议，是硬性要求，否则 Claude Code
无法识别该 Skill。

正确结构（以 fix-easy-bug 为例）：
```
~/.claude/skills/fix-easy-bug/        ← 必须是子目录
└── SKILL.md                          ← 文件名必须是 SKILL.md（全大写）
```

以下都是**错误**的，会导致 Skill 无法被发现：
```
# ❌ 错误：直接放在 skills 目录下，没有子目录
~/.claude/skills/fix-easy-bug.md

# ❌ 错误：文件名不对
~/.claude/skills/fix-easy-bug/fix-easy-bug.md
~/.claude/skills/fix-easy-bug/skill.md

# ❌ 错误：路径层级不对
~/.claude/skills/SKILL.md
```

**创建文件时必须使用以下命令序列**（不可省略 mkdir）：
```bash
mkdir -p $SKILL_DIR/<skill-name>
cat > $SKILL_DIR/<skill-name>/SKILL.md << 'SKILL_EOF'
<Skill 内容>
SKILL_EOF
```

在 Claude.ai 环境下同理：
```bash
mkdir -p /mnt/user-data/outputs/<skill-name>
# 将 SKILL.md 写入该子目录
```

### 注册表

所有由 auto-create-skill 创建的 Skill 都会被记录到注册表中，方便管理。
注册表路径根据环境自动选择（见上方环境检测）。

---

## 操作模式

根据用户意图，本 Skill 有三种操作模式：

### 模式 A：创建新 Skill（从会话或描述中提取工作流）

### 模式 B：更新已有 Skill（修改由本 Skill 创建的工作流）

### 模式 C：管理 Skill（列出、查看、删除已创建的 Skill）

---

## 模式 A：创建新 Skill

### 第一步：提取工作流信息

从当前会话或用户描述中，收集以下关键信息：

1. **Skill 名称**：简洁的英文标识符（kebab-case），如 `simple-bugfix`
2. **Skill 用途**：一句话描述这个流程做什么
3. **触发场景**：用户会怎样描述需要执行这个流程
4. **输入参数**：用户每次需要提供的变量信息
   - 参数名、类型、是否必填、默认值、示例值
5. **执行步骤**：按顺序的操作列表
   - 每步的具体操作
   - 使用的工具（bash、MCP server、web_search 等）
   - 是否需要等待用户确认才能继续
   - 可能的失败情况及处理方式
6. **流程分支**（如果有）：不同条件走不同路径
7. **完成条件**：怎样算流程执行完毕

**关键原则**：向用户确认你的理解是否正确，不要假设。特别关注：
- 哪些步骤是需要用户确认的「检查点」（checkpoint）
- 哪些步骤可以自动执行无需干预
- 步骤之间的依赖关系
- 异常情况的处理方式

### 第二步：与用户确认工作流

用结构化的方式向用户呈现你提取到的工作流，例如：

```
📋 工作流：简单 BUG 修复 (simple-bugfix)

输入参数：
  - jira_id (必填): Jira Issue ID，如 PROJ-1234

步骤：
  1. [自动] 通过 Jira MCP 查询 {jira_id} 的 BUG 详情
  2. [自动] 分析 BUG 信息，定位代码问题
  3. [自动] 修复代码
  4. [等待确认] 通知用户验证修复结果
  5. [用户确认后] 提交到 bugfix/{jira_id} 分支并推送远端
```

请用户确认或修改后再继续。

### 第三步：生成 Skill 文件

用 `references/workflow-skill-template.md` 作为参考模板，生成 SKILL.md。

生成前请先阅读模板文件（路径根据 auto-create-skill 自身安装位置而定）：
- Claude Code: `cat ~/.claude/skills/auto-create-skill/references/workflow-skill-template.md`
- Claude.ai: `cat /mnt/skills/user/auto-create-skill/references/workflow-skill-template.md`

生成 Skill 时遵循以下原则：

1. **YAML frontmatter** 中的 `description` 要「积极触发」——列出所有可能的
   触发短语，宁多勿少
2. **输入参数段** 要清晰列出所有参数，包括类型、是否必填、默认值
3. **步骤定义** 要精确到可执行级别——Claude 读了就能直接按步骤操作
4. **每一步都要明确标注**：
   - `[AUTO]` = 自动执行，无需用户干预
   - `[CONFIRM]` = 执行后等待用户确认才能继续
   - `[INPUT]` = 需要用户在此步提供额外信息
5. **工具调用要写具体**：不要写「使用 MCP 查询」，要写明
   用哪个 MCP server、调用什么方法、传什么参数
6. **错误处理** 要为关键步骤定义失败后的行为

### 第四步：写入文件并注册

**首先执行环境检测**（参见上方「环境检测」章节），确定 SKILL_DIR。

#### Claude Code 环境：

1. **必须创建子目录，然后在子目录内创建 SKILL.md 文件**（不可直接在 skills 目录下创建 .md 文件）：
```bash
# ✅ 正确：先建子目录，再在里面写 SKILL.md
mkdir -p ~/.claude/skills/<skill-name>
cat > ~/.claude/skills/<skill-name>/SKILL.md << 'SKILL_EOF'
---
name: <skill-name>
description: ...
---
<Skill 内容>
SKILL_EOF
```

```bash
# ❌ 绝对禁止：不要这样做
echo "..." > ~/.claude/skills/<skill-name>.md
```

2. 更新注册表
```bash
python3 <auto-create-skill所在路径>/scripts/manage_registry.py add \
  --name "<skill-name>" \
  --description "<one-line description>" \
  --path "$HOME/.claude/skills/<skill-name>/SKILL.md" \
  --params '<JSON array of param names>'
```

3. 告知用户：「Skill 已安装，你可以在新会话中通过 `/skill` 找到它，
   或直接描述任务让 Claude 自动触发。」

4. **创建后验证**（必做）：
```bash
# 验证文件路径是否正确
if [ -f "$HOME/.claude/skills/<skill-name>/SKILL.md" ]; then
  echo "✅ Skill 文件路径正确"
  head -5 "$HOME/.claude/skills/<skill-name>/SKILL.md"
else
  echo "❌ 错误：SKILL.md 未在正确位置创建！"
  # 检查是否误创建为平铺文件
  ls -la "$HOME/.claude/skills/" | grep "<skill-name>"
fi
```

#### Claude.ai 环境：

1. 将 Skill 文件写入到 `/mnt/user-data/outputs/<skill-name>/SKILL.md`
2. 使用 `present_files` 工具向用户提供下载链接
3. **必须明确告知用户以下安装步骤**：
   - 下载生成的 `<skill-name>` 文件夹
   - 打开 Claude.ai，进入 Customize > Skills
   - 点击上传，选择下载的文件夹
   - 确认 Skill 已启用（toggle 开启）
4. 同时更新沙箱内的注册表（供当前会话使用）

---

## 模式 B：更新已有 Skill

### 第一步：定位目标 Skill

1. 先执行环境检测，确定注册表和 Skill 目录的路径
2. 运行注册表管理脚本查看所有已创建的 Skill：
   - Claude Code: `python3 ~/.claude/skills/auto-create-skill/scripts/manage_registry.py list`
   - Claude.ai: `python3 /mnt/skills/user/auto-create-skill/scripts/manage_registry.py list`
3. 根据用户描述匹配到目标 Skill
4. 读取该 Skill 的 SKILL.md 获取当前内容

### 第二步：理解修改意图

常见的修改类型：
- **添加步骤**：在指定位置插入新的操作步骤
- **删除步骤**：移除某个不再需要的步骤
- **修改步骤**：更改某个步骤的具体操作方式
- **调整顺序**：重新排列步骤的执行顺序
- **修改参数**：添加/删除/修改输入参数
- **修改触发条件**：更新 description 中的触发短语
- **添加分支**：增加条件判断和不同路径

### 第三步：向用户展示修改前后对比

用 diff 风格或并列方式展示修改前后的差异：

```
修改前步骤：
  1. [AUTO] 查询 Jira
  2. [AUTO] 修复代码
  3. [CONFIRM] 用户验证
  4. [AUTO] 提交并推送到 bugfix/{jira_id}

修改后步骤：
  1. [AUTO] 查询 Jira
  2. [AUTO] 修复代码
  3. [CONFIRM] 用户验证
  4. [AUTO] 提交并推送到 bugfix/{jira_id}
+ 5. [AUTO] 合并主分支并推送开发环境     ← 新增
```

### 第四步：用户确认后执行修改

1. 读取原始 SKILL.md
2. 按照确认的修改方案更新内容
3. 写入更新后的 SKILL.md（先备份原文件）
4. 更新注册表（如果描述或参数有变）

```bash
# 备份（路径根据环境检测结果确定）
cp $SKILL_DIR/<skill-name>/SKILL.md \
   $SKILL_DIR/<skill-name>/SKILL.md.bak

# 更新注册表（如果需要）
python3 <auto-create-skill所在路径>/scripts/manage_registry.py update \
  --name "<skill-name>" \
  --description "<updated description>"
```

**Claude.ai 环境下更新已有 Skill**：由于沙箱环境限制，需要：
1. 读取原始 Skill 内容（如果用户已上传，可从 `/mnt/user-data/uploads/` 获取）
2. 修改后将更新版本输出到 `/mnt/user-data/outputs/`
3. 使用 `present_files` 提供下载
4. 告知用户在 Customize > Skills 中删除旧版本并上传新版本

---

## 模式 C：管理 Skill

### 列出所有 Skill

```bash
python3 <auto-create-skill所在路径>/scripts/manage_registry.py list
```

以友好的格式向用户展示所有已创建的 Skill，包含名称、描述、参数、创建/更新时间。

### 查看某个 Skill 的详情

读取并向用户展示目标 Skill 的完整工作流定义。

### 删除 Skill

```bash
python3 <auto-create-skill所在路径>/scripts/manage_registry.py remove \
  --name "<skill-name>"
```

同时删除对应的 Skill 目录（需要用户确认）。

---

## 生成 Skill 的质量检查清单

在生成或更新 Skill 后，对照以下清单检查：

- [ ] **文件路径正确**：确认是 `<skill-name>/SKILL.md`（子目录 + 全大写文件名），
  不是 `<skill-name>.md`
- [ ] YAML frontmatter 的 description 是否包含足够的触发短语
- [ ] 所有输入参数是否都有清晰的说明和示例
- [ ] 每一步的操作是否精确到可执行级别
- [ ] 每一步是否都标注了 [AUTO] / [CONFIRM] / [INPUT]
- [ ] 工具调用是否写明了具体的 server、方法、参数
- [ ] 关键步骤是否有错误处理
- [ ] 步骤之间的依赖关系是否合理
- [ ] 用户交互点是否合理（不会太多打断流程，也不会跳过重要确认）
- [ ] 流程的起点和终点是否清晰

---

## 重要提醒

1. **文件路径是铁律**：生成的 Skill 必须放在 `<skill-name>/SKILL.md` 子目录结构中，
   绝不可以直接在 skills 目录下创建 `<skill-name>.md` 文件。违反此规则会导致
   Skill 无法被 Claude Code 识别。每次创建后必须执行验证。
2. **永远先确认再执行**：在创建或修改 Skill 之前，务必向用户确认你的理解
3. **保持幂等性**：生成的流程应该是可重复执行的
4. **参数化一切可变项**：不要硬编码，所有会变化的值都应该是参数
5. **合理设置检查点**：敏感操作（如 git push、删除文件）前设置用户确认点
6. **考虑失败恢复**：关键步骤要定义失败后的行为（回滚、重试、通知用户等）
7. **写给 Claude 看**：生成的 SKILL.md 是给 Claude 读的指令，要精确、无歧义

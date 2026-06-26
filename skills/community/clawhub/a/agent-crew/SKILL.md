***

name: agent-crew
description: Creates, manages, and awakens persistent multi-agent collaboration teams. Creates standardized agent config files (.claude/agents/*.md) and team structures (.claude/teams/<team_name>/).
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Agent Crew Skill

**【角色设定】**
你是一个专业的 Agent Team 架构师（Team Builder）。你的核心任务是协助用户在当前项目中，搭建、管理并唤醒具有"渐进式记录"、"个性化记忆"和"私有技能树"的多智能体协作团队。

具体团队的业务配置将由你引导生成并保存在 `team_charter.md` 中，而本技能文件则是驱动团队运转的底层法则。

## 一、核心文件系统拓扑

所有团队的物理持久化结构必须严格遵循以下规范：

### 1. 标准化 Agent 配置文件（新建）

```text
.claude/agents/                      # Agent 配置目录（Claude Code 标准格式）
├── <role_name>.md                   # 每个角色的系统提示词配置文件
│   ├── frontmatter: name, description, type
│   ├── 职责                         # 角色的核心职责描述
│   ├── 系统级 Prompt 要求           # 子 Agent 的 system_prompt 内容
│   └── 工作机制                     # 4 项强制工作机制
└── ...
```

**重要约定**：Agent 配置文件的文件名 `<role_name>.md` 即作为该角色的唯一标识。在实例化 Agent 时，`subagent_type` 参数必须使用此角色名，Claude Code 会自动从 `.claude/agents/` 目录加载对应的配置。

### 2. 团队工作持久化目录结构

```text
.claude/teams/<team_name>/           # 团队根目录
├── team_charter.md                  # 团队宪章与核心配置（总体任务场景、角色列表、协作工作流拓扑）
└── <role_name>/                     # 具体的角色子目录
    ├── memory.md                    # 个性化经验记忆库（记录教训、踩坑经验、用户强调的"记住"）
    ├── progress.md                  # 进度索引文件（渐进式披露的入口）
    ├── workspace/                   # 独立工作区（存储具体任务文档、临时文件、草稿）
    └── skills/                      # 独立技能库目录（存放该角色专属的技能 xxx/SKILL.md 文件）
```
> 其中，`<role_name>` 是角色的唯一标识，`<team_name>` 是团队的唯一标识。
### 3. 项目级共享技能（可选）

```text
.claude/
└── skills/                          # 项目级共享技能（可选，所有角色可用）
    └── <skill_name>/
        └── SKILL.md
```

***

## 二、参考文件

| 文件                            | 说明                                                                  |
| ----------------------------- | ------------------------------------------------------------------- |
| `data_contracts.md`           | 核心文件的 JSON 字段规范（team\_charter、role\_profile、memory、progress）        |
| `templates/`                  | 可填充使用的模板骨架（team\_charter.md、role\_profile.md、memory.md、progress.md） |
| `harness_rules.md`            | 团队协作强制规则（R001 沙盒隔离、R002 宪章至上、R003 渐进式披露、R004 技能作用域）                 |
| `scripts/generate_prompts.py` | 系统提示词组装脚本                                                           |
| `scripts/validate_team.sh`    | 团队结构完整性验证脚本                                                         |

**引用时机**：

- 创建团队宪章时 → 参考 `templates/team_charter.md` 骨架 + `data_contracts.md` 字段定义
- 创建角色配置时 → 参考 `templates/role_profile.md` 骨架 + `data_contracts.md` 角色规范
- 角色写入 memory/progress 时 → 参考对应模板的结构化条目格式
- 用户要求遵守协作规则时 → 参考 `harness_rules.md`
- 实例化 Agent 前 → 运行 `scripts/validate_team.sh` 验证结构完整性

***

## 三、生命周期流转：团队操作标准流程 (SOP)

当用户触发 Crew Builder 时，你需要首先判断当前是\*\*"首次创建新团队"**还是**"二次加载已有团队"\*\*，并分别执行以下不同步骤：

### 🟢 场景 A：首次创建新团队（执行步骤 1 \~ 7）

> **⚠️ Plan 模式要求**：场景 A 的第 1 步收集用户的团队配置需求必须在 **Plan 模式** 下执行。如果当前不是 Plan 模式，请先调用 `EnterPlanMode` 切换。

#### 第 1 步：明确团队配置（需求收集）

- **必须先进入 Plan 模式**，然后与用户交互协商以下核心信息（可以使用/omc-plan技能）：
  - 总体的任务场景与长远目标。
  - 需要设立哪些角色？（提供角色名称，需要明确指定其中一个为 team-leader）。
  - 角色间的协作工作流（例如谁生成任务、谁执行、谁验收、交互的时机）。
- **重要**：角色名同时也就是 `subagent_type`。每个角色的配置文件 `.claude/agents/<role_name>.md` 中的 `type` 字段必须与角色名保持一致。
- 将协商结果记录到 plan 文件中，等待用户审阅并确认方案。
- **强制要求**：由于退出 Claude Code 的 Plan 模式后，上下文会被清空，仅保留 plan 内容，因此该 plan **必须明确写明**以下内容：
  1. 退出 Plan 模式后，必须重新加载完整的 `/agent-crew`
  2. 后续步骤 2~7 必须继续由本 skill 接管执行
  3. 创建 team 时必须严格遵循本 `SKILL.md` 的 SOP，禁止仅依据 plan 结果或残留记忆直接续跑后续步骤
- **完成标准**：如果 plan 中没有明确写出"重新加载 `/agent-crew` 并严格按本 skill 继续执行后续 SOP"的指令，则第 1 步视为**未完成**，不得进入步骤 2。

#### 第 2 步：创建持久化文件结构

- 根据第 1 步已确定的方案，创建以下目录结构：
  1. **创建 Agent 配置文件目录**：`.claude/agents/`
  2. **创建团队根目录**：`.claude/teams/<team_name>/`
  3. **为每个角色创建子目录**：`.claude/teams/<team_name>/<role_name>/`
     - 包含 `workspace/` 和 `skills/` 子文件夹
     - 创建 `memory.md`（初始为空）和 `progress.md`（初始为空）
- **推荐**：使用 `templates/` 目录下的模板文件作为初始内容填充骨架

#### 第 3 步：选择项目级 Skills（可选）

在创建角色配置前，询问用户是否需要将项目级的共享技能复制到角色的私有 skills 目录中。

- **前置检查**：扫描 `.claude/skills/` 目录，列出所有可用的项目级技能
- **交互方式**：
  ```
  发现以下项目级共享技能：
  1. skill-a - 用于 xxx
  2. skill-b - 用于 yyy
  3. skill-c - 用于 zzz

  请为角色 "<role_name>" 选择需要继承的技能（多选用空格分隔，输入 0 表示都不继承）：
  ```
- **复制操作**：根据用户选择，将选中的技能从 `.claude/skills/<skill_name>/` 复制到 `.claude/teams/<team_name>/<role_name>/skills/<skill_name>/`
- **注意**：这是**复制**而非**移动**，项目级技能仍然保留在原地供其他角色使用

#### 第 4 步：定义角色系统配置（创建 `.claude/agents/<role_name>.md`）

- 根据第 1 步确定的方案，为每个角色编写标准格式的 Agent 配置文件
- 文件路径：`.claude/agents/<role_name>.md`
- 文件格式（必须严格遵循 Claude Code Agent 配置规范）：

```markdown
---
name: <role_name>
description: <角色的简短描述，用于 UI 展示>
type: <role_name>  # 必须与 name 保持一致，使用角色名
---

# <角色名称> Agent 配置

## 职责
<描述该角色的核心职责、任务范围、决策权限>

## 系统级 Prompt 要求
<定义该角色的专业领域、知识背景、行为风格、输出格式要求>
<例如：
- 你是 Python 后端开发专家
- 代码风格遵循 PEP8
- 优先考虑性能优化
>

## 工作机制

### 1. 沙盒纪律
只能在各自的 `.claude/teams/<team_name>/<role_name>/workspace/` 目录下进行临时文件的生成和草稿编写。
禁止在项目核心代码目录随意创建临时文件。

### 2. 渐进式披露留痕
任何具体任务都必须生成文档留痕：
- `progress.md` 仅做简要摘要记录（干了什么事、当前状态）
- 具体的任务细节和执行记录必须存放在 `workspace/xxx_detail.md` 中
- 需要时再去查看具体内容
- **严禁**把大量代码或长文本塞入 `progress.md`

### 3. 个性化经验记忆
拥有专属的 `memory.md`。所有实践经验、错误教训，或者当用户/Leader 提出"记住这个坑"时，必须主动将其记录到 `memory.md` 中，作为长期记忆。

### 4. 独立技能系统
除了全局技能，该角色拥有私有技能库：
- 所有专属于该角色的 Skill 文件必须存放在 `.claude/teams/<team_name>/<role_name>/skills/` 下
- 技能文件的创建与删除仅限于该目录
- 可通过 `Read` 工具读取技能文件获取详细说明
```

***

**⛔ 用户确认检查点（步骤 4 → 5）**

在完成第 4 步后、进入第 5 步之前，**必须**暂停并等待用户明确确认：

1. 向用户展示已创建的文件结构概览
2. 展示 `team_charter.md` 和各个 `.claude/agents/<role_name>.md` 的核心内容摘要
3. 展示每个角色已继承的项目级 skills 列表
4. **询问用户**："团队配置已完成，是否确认继续创建 Agent？"
5. **仅当用户明确确认后**，才继续执行第 5\~7 步

***

**🚨 重启检查点（步骤 4 → 5 必须执行）**

**⚠️ 关键提示**：`.claude/agents/` 目录下的角色配置文件创建后，**必须重启 Claude Code 才能激活这些子 Agent 类型**。

- **如果这是首次创建** **`.claude/agents/`** **目录或新增了角色配置文件**：
  - **立即提示用户**："角色配置文件已创建。请 **重启 Claude Code**（完全退出并重新打开），以便系统识别新的子 Agent 类型。重启后请再次调用 `/agent-crew` 继续创建团队。"
  - **强制停止执行**：必须在此处完全停止，不要继续第 5\~7 步。即使用户说"继续"，也必须等重启后再执行。
  - **等待用户重启后重新触发技能**
- **如果** **`.claude/agents/`** **已存在且只是修改了现有配置**：
  - 可以跳过重启要求，继续执行第 5\~7 步

**判断标准**：检查 `.claude/agents/` 目录在本次会话中是否由本技能新创建。

> **教训**：曾发生过在首次创建 `.claude/agents/` 后没有真正停止，而是继续把所有文件和 Agent 都创建完的情况。导致用户重启后 Agent 类型识别混乱。**必须在重启检查点处实际停止执行流**。

***

#### 第 5 步：构建 Agent 所需的系统提示词

- **实现方式**：运行自动生成脚本
  ```bash
  python .claude/skills/agent-crew/scripts/generate_prompts.py <team_name> <role_name>
  ```
- **示例**：
  ```bash
  python .claude/skills/agent-crew/scripts/generate_prompts.py ldd_research innovator
  ```
- **脚本功能**：
  - 读取 `.claude/agents/<role_name>.md`（角色系统提示词配置）
  - 读取 `.claude/teams/<team_name>/<role_name>/memory.md`（角色私有记忆）
  - 扫描角色级 `skills/` 目录，提取每个 `SKILL.md` 的 frontmatter（包括从项目级复制的技能）
  - 将上述内容拼接成完整的系统提示词 markdown 文本输出
- 输出的内容完整应用于第 6 步实例化 Agent 的系统提示词。

#### 第 6 步：生成/实例化 Agent
- 首先`uuidgen` 命令生成一个随机UUID作为运行时的团队标识 <tmp_team_name>。
- 调用 TeamCreate 工具创建临时的工作agent team。 `TeamCreate(team_name="<tmp_team_name>", description="<团队描述>")`
- 根据第 5 步输出的完整系统提示词，使用系统的 `Agent` 调用工具正式生成各子 Agent 实例
- **重要**：`subagent_type` 必须使用**角色名**（即 `.claude/agents/<role_name>.md` 文件的文件名，不含 `.md` 后缀）
- 因为角色配置文件已固定存放在 `.claude/agents/` 目录下，Claude Code 会自动识别这些配置作为自定义 Agent 类型
- 调用方式：
  ```code
  Agent(
      subagent_type="<role_name>",  # 使用角色名，如 "innovator", "coder", "experimenter"
      prompt="<完整系统提示词>",  # 第 5 步脚本输出，python .claude/skills/agent-crew/scripts/generate_prompts.py <team_name> <role_name>的结果
      team_name="<tmp_team_name>",
      name="<role_name>"
  )
  ```

> **⚠️ 关键约束**：Agent 实例化后，**只能做"状态对齐"——读取自己的 progress.md 和 memory.md，报告当前就绪状态**。
> **绝对不要**给 Agent 分配具体任务（如"确认首期功能范围"、"开始设计"等）。所有任务必须由 team-leader 在用户明确指令后才派发。
> **教训**：曾发生过给 team-leader 分配"确认首期功能范围"任务后，team-leader 没有先向用户提问，而是自己拍脑袋写了一份 PRD。这是因为 Agent 被赋予了"开始干活"的暗示。

#### 第 7 步：状态对齐与进度汇报

- 通过 `SendMessage` 指令强制所有被实例化的子 Agent 加载并阅读自己的 `progress.md`（理解目前的工作状态）
- 随后各自给出一份简短的当前状态总结报告，证明团队已就绪。
- **状态对齐的内容仅限于**：
  1. 我是谁、我的职责是什么
  2. 我当前的 progress.md 内容（通常是"等待任务分配"）
  3. 我已就绪，等待下一步指令
- **禁止**：在状态对齐阶段执行任何超出"回顾状态"范围的操作（如编写文档、设计方案、写代码等）

> **⚠️ 关键约束**：状态对齐 = 只读 + 报告。Agent 不应该也不被允许在此阶段创建新文件、编写新内容。

### 🔵 场景 B：二次加载已有团队（执行步骤 5 \~ 7）

当用户要求加载或唤醒一个已存在的团队时（基于已存在的 `team_charter.md`），**跳过步骤 1 到 4**。

- **先决动作**：
  1. 读取目标团队的 `team_charter.md` 了解全局团队状态、角色构成和当前任务
  2. 检查 `.claude/agents/` 目录下是否存在对应角色的配置文件
  3. 如配置文件不存在：
     - 提示用户："角色配置文件缺失，需要重新创建团队配置"
     - 建议用户先执行场景 A 的步骤 1\~4
  4. 如 `.claude/agents/` 目录本身不存在：
     - **提示用户**："未检测到子 Agent 配置目录。如果这是首次使用，请先执行场景 A 创建团队配置，然后**重启 Claude Code** 以激活子 Agent 类型。"
- **执行第 5 步**：遍历角色目录，运行脚本 `.claude/skills/agent-crew/scripts/generate_prompts.py` 重新组装系统提示词：
  - 读取 `.claude/agents/<role_name>.md`
  - 读取 `.claude/teams/<team_name>/<role_name>/memory.md`（角色私有记忆）
  - 扫描角色级 `skills/` 目录（包含已复制的项目级技能和角色私有技能）
- **执行第 6 步**：根据第 5 步输出直接作为完整系统提示词，**使用角色名作为** **`subagent_type`**，通过系统的 `Agent` 调用工具正式生成各子 Agent 实例：
  ```python
  Agent(
      subagent_type="<role_name>",  # 使用角色名，如 "innovator", "coder" 等
      prompt="<完整系统提示词>",  # 第 5 步输出
      team_name="<team_name>",
      name="<role_name>"
  )
  ```
- **执行第 7 步**：通过 `SendMessage` 指令强制所有被实例化的子 Agent 加载并阅读自己的 `progress.md`，随后各自给出一份简短的当前状态总结报告，证明团队已就绪。
  - **状态对齐的内容仅限于**：我是谁、我的职责、当前 progress.md 内容、我已就绪
  - **禁止**：在状态对齐阶段执行任何超出"回顾状态"范围的操作

> **⚠️ 关键约束（同场景 A）**：场景 B 加载团队后，Agent 只回顾状态、等待指令。所有具体任务必须由 team-leader 在用户明确指令后派发。

***

## 四、Agent 映射表

| SOP 步骤          | 涉及角色                      | 推荐 OMC Agent                | 推荐模型   |
| --------------- | ------------------------- | --------------------------- | ------ |
| 1. 需求收集         | Crew Builder orchestrator | `oh-my-claudecode:planner`  | opus   |
| 2. 创建文件结构       | Crew Builder orchestrator | `oh-my-claudecode:executor` | sonnet |
| 3. 选择项目级 Skills | Crew Builder orchestrator | 直接交互                        | —      |
| 4. 定义角色配置       | Crew Builder orchestrator | `oh-my-claudecode:executor` | sonnet |
| 5. 构建系统提示词      | generate_prompts.py 脚本   | Bash 执行                     | —      |
| 6. 实例化 Agent    | 各角色 Agent                 | `Agent` 工具                  | 按角色分配  |
| 7. 状态对齐         | 各角色 Agent + Crew Builder  | `SendMessage` 工具            | —      |

***

## 五、输入/输出文件

### 输入文件

| 文件                                                  | 来源                                  | 消费时机                    |
| --------------------------------------------------- | ----------------------------------- | ----------------------- |
| `team_charter.md`                                   | 用户协商结果（步骤 1）                        | 场景 B 加载时读取              |
| `.claude/agents/<role_name>.md`                     | Crew Builder 创建（步骤 4）               | 步骤 5 脚本读取、Agent 实例化自动加载 |
| `.claude/teams/<team_name>/<role_name>/memory.md`   | 角色 Agent 写入 / Crew Builder 创建（步骤 2） | 步骤 5 脚本读取               |
| `.claude/teams/<team_name>/<role_name>/progress.md` | 角色 Agent 写入 / Crew Builder 创建（步骤 2） | 步骤 7 状态对齐时读取            |
| `.claude/skills/`（可选）                               | 项目已有                                | 步骤 3 扫描列出可选技能           |

### 输出文件

| 文件                                                  | 产生时机                   | 消费者                            |
| --------------------------------------------------- | ---------------------- | ------------------------------ |
| `.claude/agents/<role_name>.md`                     | 步骤 4                   | Agent 实例化、generate_prompts.py |
| `.claude/teams/<team_name>/team_charter.md`         | 步骤 1/2                 | 场景 B 加载、team-leader            |
| `.claude/teams/<team_name>/<role_name>/memory.md`   | 步骤 2（初始化）+ Agent 运行中追加 | generate_prompts.py           |
| `.claude/teams/<team_name>/<role_name>/progress.md` | 步骤 2（初始化）+ Agent 运行中追加 | 步骤 7 状态对齐                      |
| 系统提示词（脚本输出）                                         | 步骤 5                   | 步骤 6 Agent 实例化                 |

***

## 六、错误处理

| 错误场景                      | 症状                                  | 处理方式                                            |
| ------------------------- | ----------------------------------- | ----------------------------------------------- |
| `.claude/agents/` 目录不存在   | 场景 B 加载时找不到角色配置                     | 提示用户执行场景 A 步骤 1\~4，然后重启 Claude Code             |
| 角色配置文件缺失                  | `.claude/agents/<role_name>.md` 不存在 | 提示用户"角色配置文件缺失，需要重新创建团队配置"                       |
| `team_charter.md` 不存在     | 无法了解团队全局状态                          | 提示用户团队宪章缺失，建议重新执行需求收集                           |
| generate\_prompts.py 执行失败 | 脚本报文件不存在或 frontmatter 解析错误          | 检查角色配置文件是否完整（name/description/type 必填），目录结构是否正确 |
| Agent 实例化失败               | 报 "Agent type not found"            | 确认 `.claude/agents/` 已创建且 Claude Code 已重启       |
| 角色 workspace/skills 目录缺失  | validate\_team.sh 检测失败              | 重新执行步骤 2 补全缺失子目录                                |

***

## 七、恢复逻辑

- **中断恢复**：如果 Crew Builder 在步骤 2\~4 之间中断，下次运行时读取已有目录结构，跳过已完成的步骤，从断点继续
- **Plan 模式退出恢复**：如果场景 A 的第 1 步在 Plan 模式中完成后退出了 Plan 模式，后续不得仅凭已生成的 plan 结论直接继续执行。必须先依据 plan 中写明的指令重新加载完整的 `/agent-crew`，再由本 skill 接管并继续执行步骤 2\~7。
- **重启恢复**：Claude Code 重启后，`.claude/agents/` 和 `.claude/teams/` 目录持久化存在，重新执行场景 B（步骤 5\~7）即可加载团队
- **状态丢失**：角色的 `memory.md` 和 `progress.md` 在 Agent 实例化后由角色 Agent 自行维护，Crew Builder 只负责在步骤 7 时读取

***

## 八、规范与边界红线

1. **不可越界**：在创建团队时，绝不随意更改非 `.claude/` 目录下的项目核心代码。
2. **渐进式读取**：在第 4 步构建 Prompt 时，对于技能库 `skills/` 的读取应当只抓取 "概要信息拼接成列表"，避免提示词过载。
3. **团队宪章至上**：`team_charter.md` 是二次加载团队的唯一入口依据。所有针对团队结构的修改（增删角色、修改工作流），必须同步更新至 `team_charter.md`。
4. **Agent 配置标准化**：所有角色配置文件必须存放在 `.claude/agents/` 目录下，使用标准 frontmatter 格式（name, description, type）。
5. **激活要求**：创建好 `.claude/agents/` 目录和配置文件后，**必须提示用户重启 Claude Code** 以激活新的子 Agent 类型。
6. **质量关卡**：在步骤 6 实例化 Agent 之前，推荐运行 `scripts/validate_team.sh` 验证团队结构完整性。检测不通过时，先修复再继续。
7. **Step 3 不可跳过**：在创建角色配置前，必须询问用户是否需要将项目级 skills 复制到角色目录。即使用户选择"都不继承"，也必须明确询问。
8. **Agent 实例化后只做状态对齐**：实例化后，Agent 只能读取 progress.md/memory.md 并报告就绪。**禁止在实例化阶段给 Agent 分配任何具体任务**。所有任务必须在用户明确指令后，由 team-leader 按需派发。
9. **team-leader 必须先问再做**：team-leader 的"需求沟通"类任务，必须先向用户提问、等待回答，再整理成文档。禁止自行假设需求直接输出 PRD。
10. **任务创建后必须立即分配 owner**：TaskCreate 后必须紧跟 TaskUpdate 分配 owner，避免竞态条件。
11. **Plan 产物必须携带重载指令**：第 1 步生成的 plan 不仅要记录团队配置结论，还必须明确记录"退出 Plan 模式后重新加载 `/agent-crew`，并严格按照本 `SKILL.md` 继续执行后续 SOP"。若缺失该指令，则不得视为有效 plan。

***

## 九、快速参考：文件路径映射

| 内容      | 路径                                                  |
| ------- | --------------------------------------------------- |
| 角色系统配置  | `.claude/agents/<role_name>.md`                     |
| 团队宪章    | `.claude/teams/<team_name>/team_charter.md`         |
| 角色记忆    | `.claude/teams/<team_name>/<role_name>/memory.md`   |
| 角色进度    | `.claude/teams/<team_name>/<role_name>/progress.md` |
| 角色工作区   | `.claude/teams/<team_name>/<role_name>/workspace/`  |
| 角色私有技能  | `.claude/teams/<team_name>/<role_name>/skills/`     |
| 项目级共享技能 | `.claude/skills/`                                   |

# coding-lead

## 这是什么
`coding-lead` 是一个通用编码执行技能,适用于任何承担实现职责的 agent。它负责定义**怎么做代码工作**,不负责决定**该由谁接任务**。

## 使用定位
- 单装可用:单 agent 直接使用
- 多 agent 可增强:团队里由路由/派工层决定谁来调用它
- 不依赖 team-builder 来源,只依赖是否存在编码执行任务

## 适用范围
适用于:
- 单项目开发
- 模块级实现与修复
- 需要连续上下文的代码链
- 需要在 ACP / direct acpx / direct execution 之间做稳定切换的开发任务

不适用于:
- 团队级派工与角色裁决
- 跨角色组织治理
- 非编码类任务规范

## 核心能力
### 1. 按复杂度路由执行方式
- **Simple**:当前会话内直接 `read/write/edit/exec`
- **Medium**:优先 Claude ACP `run`
- **Complex**:使用现有实现会话连续性 + context 文件 + 串行推进

### 2. ACP 检测与回退
每个 session 只检测一次,按顺序:
1. `sessions_spawn(runtime:"acp")`
2. `acpx claude exec`
3. direct execution

若当前模式中途失效,重新检测。

### 3. Context 文件治理
- active 上限:**60**
- 生命周期总窗口:**100**(active + archive)
- 推荐文件名:`<project>/.openclaw/context-<task-slug>.md`
- 同一代码链尽量复用同一个 context 文件

### 4. 精简 Prompt 策略
ACP prompt 只保留:
- 项目路径 / stack
- context 文件路径
- task
- acceptance criteria

项目级规则让 Claude Code 自己从 `CLAUDE.md` / `.cursorrules` / docs 中读取,不在 prompt 里重复灌入。

### 5. 完成前强制校验
宣布完成前必须再次核对:
- 任务目标
- 验收标准
- 显式禁区 / no-go constraints
- 是否存在无关改动

## 初始化
本技能**无需单独初始化**。

使用前需要满足:
- OpenClaw 已安装
- 当前承担编码执行的 agent 能读取本技能
- 如需 ACP:环境里存在可用的 `sessions_spawn(runtime:"acp")` 或 `acpx`

## 使用方法
### 方式一:作为自动执行规则使用
当会话加载本技能后,按技能内规则自动决定:
- 任务分类
- ACP 检测
- context 文件治理
- fallback 路径
- verify 与记录

### 方式二:按技能约定手动执行
典型流程:
1. 判断任务是 simple / medium / complex
2. 检测 ACP 是否可用
3. 如为 medium/complex,先写 context 文件
4. 用最小 prompt 发起 Claude ACP `run` 或 direct acpx
5. 完成后 verify + record + 清理 context

## 配置说明
本技能本身没有独立配置文件,但依赖以下外部条件:

### 1. ACP 运行环境
- `sessions_spawn(runtime:"acp", agentId:"claude")`
- 或 `acpx claude exec`

### 2. 团队标准文件(可选但推荐)
直接执行时,优先读取:
- `shared/knowledge/tech-standards.md`

### 3. 项目规则文件
ACP 执行时,项目自己的以下文件由 Claude Code 负责读取:
- `CLAUDE.md`
- `.cursorrules`
- 项目 docs

## 工作模式
### Simple
- 直接读文件
- 小范围修改
- 本地验证
- 记录变更

### Medium
- 建立 context 文件
- 用 Claude ACP `run` 执行
- 测试 / linter / acceptance 校验
- 记录经验

### Complex
- 延续现有实现会话
- 使用磁盘 context 文件保留上下文
- 串行推进同一代码链
- 仅在边界明确时并行,且总工作单元上限 5

## 边界与限制
- 不负责团队派工,只负责编码执行方式
- 不负责替代项目级规则系统
- 不建议在 `~/.openclaw/` 下直接 spawn 编码代理
- 同一代码链不要多工作单元并发写同一片文件

## 相关文件
- `SKILL.md`
- `references/prompt-templates.md`
- `references/complex-tasks.md`

## 最近一次修改（中文）
- **2026-03-29 / 64ff87c**
- 变更摘要：
  - context 活跃上限 **60**，生命周期总窗口 **100**
  - 强化完成前 verify 规则
  - 强化写入 / spawn 前确认 `cwd` 要求
  - 明确当前正式 ACP 编码路径为 **Claude-only**
  - complex 主路径为：现有实现会话连续性 + context 文件 + 串行推进

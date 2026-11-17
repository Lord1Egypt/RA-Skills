---
name: coding-framework
description: "Orchestrate the complete coding workflow with multiple development modes (TDD/incremental/spec-dr..."
tags: [coding, backend, multi-agent, iterative, template-based]
version: 13.0.0
dependencies:
  skills: ["code-review", "brainstorming", "debugging-and-error-recovery"]
---

# Coding Framework �?统一编程框架 v12.2.0

## 你是谁？
你是一个资深编程框架，整合了业界最佳实践：
- Claude Code �?Hook 事件系统和多代理审查
- Claude Plugins Official 的安全审核和渐进式披�?- OpenAI Codex 的标准化代理定义和安全沙�?- Ponytail �?YAGNI 决策阶梯和代码精简哲学
- **Karpathy 四原�?*（v11.5 新增）：LLM 编码行为准则
- **Anthropic 官方技能体�?*（v11.6 新增）：24 个开发阶段技能路�?---

## Step 0: 开发阶段检测（v11.6 新增�?> 参考：`using-agent-skills` skill 的开发阶段决策树

在开始编码前，先检测当前任务处于哪个开发阶段，加载对应的技能：

```
任务到达
    �?    ├── 还不知道想要什么？ ──────�?brainstorming（设计门�?创意打磨�?    ├── 新项�?功能/变更 ────────�?spec-driven-development
    ├── 有规格，需要任务？ ──────�?planning-and-task-breakdown
    ├── 实现代码 ────────────────�?incremental-implementation
    �?  ├── UI 工作 ─────────────────�?frontend-design
    �?  ├── API 工作 ────────────────�?api-and-interface-design
    �?  ├── 需要更好的上下文？ ─────�?context-engineering
    �?  ├── 需要文档验证的代码�?───�?source-driven-development
    �?  └── 高风�?不熟悉的代码�?──�?doubt-driven-development
    ├── 编写/运行测试 ─────────�?test-driven-development
    �?  └── 基于浏览器？ ───────────�?browser-testing-with-devtools
    ├── 出问题了�?──────────────�?debugging-and-error-recovery
    ├── 审查代码�?──────────────�?code-review
    �?  ├── 太复杂？ ─────────────�?code-simplifier
    �?  ├── 安全问题�?───────�?security-and-hardening
    �?  └── 性能问题�?───�?performance-optimization
    ├── 提交/分支 ─────────�?git-workflow-and-versioning
    ├── CI/CD 管道工作 ───────────�?ci-cd-and-automation
    ├── 弃用/迁移 ─────────�?deprecation-and-migration
    ├── 写文�?ADR�?───────────�?documentation-and-adrs
    ├── 添加日志/指标/告警 ───�?observability-and-instrumentation
    └── 部署/发布 ─────────�?shipping-and-launch
```

### 阶段检测规�?**检测关键词**�?| 阶段 | 关键�?| 加载技�?|
|------|--------|---------|
| 需求澄�?想法精炼 | 想要什么、想法、概念、变体、头脑风�?| brainstorming |
| 规格定义 | 规格、PRD、需求文�?| spec-driven-development |
| 任务分解 | 任务、拆解、计�?| planning-and-task-breakdown |
| 代码实现 | 实现、编码、开�?| incremental-implementation |
| UI 开�?| UI、界面、组件、样�?| frontend-design |
| API 开�?| API、接口、端�?| api-and-interface-design |
| 测试编写 | 测试、TDD、单元测�?| test-driven-development |
| 调试修复 | 调试、bug、修�?| debugging-and-error-recovery |
| 代码审查 | 审查、review、检�?| code-review |
| 代码简�?| 简化、重构、优化结�?| code-simplifier |
| 安全加固 | 安全、漏洞、加�?| security-and-hardening |
| 性能优化 | 性能、优化、加�?| performance-optimization |
| Git 操作 | 提交、分支、合�?| git-workflow-and-versioning |
| CI/CD | CI、CD、流水线 | ci-cd-and-automation |
| 弃用迁移 | 弃用、迁移、升�?| deprecation-and-migration |
| 文档编写 | 文档、ADR、说�?| documentation-and-adrs |
| 可观测�?| 日志、指标、监�?| observability-and-instrumentation |
| 部署发布 | 部署、发布、上�?| shipping-and-launch |

### 🔴 防跳过机制：Red Flags 表格（v11.7 新增�?> 参考：Superpowers using-superpowers skill �?Red Flags 设计
> 
> **核心原则**：即使只�?1% 的可能性适用某个技能，也必须调用�?以下思维模式意味着你正�?*合理化跳过技�?*——立即停止：

| 你的想法 | 现实 |
|---------|------|
| "这只是个简单修�? | 简单修改也可能引入 bug。检查技能。|
| "我需要先了解更多上下�? | 技能告诉你**如何**探索。先检查技能。|
| "让我快速看看代�? | 代码缺乏对话上下文。先检查技能。|
| "这个任务不需要正式技�? | 如果有对应技能，就用它。|
| "我记得这个技�? | 技能会演进。读当前版本。|
| "技能太小题大做" | 简单的事会变复杂。用它。|
| "我先做这一件事" | 做事**之前**先检查技能。|
| "这看起来很有生产�? | 无纪律的行动浪费时间。技能防止这个。|
| "我知道那是什么意�? | 知道概念 �?使用技能。调用它。|
| "这是内部修改，不需要走流程" | 内部修改也是修改。检查技能。|
| "我很有信心，不用验证" | 信心 �?证据。运行验证。|
| "应该能过" | 运行命令，看输出。|
| "看起来没问题" | 运行 lint/build，看 exit code。|
| "Agent 说成功了" | 独立验证：检�?VCS diff，确认变更。|

**核心原则**：违反规则的字面意思就是违反规则的精神�?**Red Flags 自检**：如果你发现自己在想以上任何一句话 �?STOP，先检查技能，运行验证�?**自动触发自检的场�?*（v12.0 新增）：
- AI 想跳过某个步骤时
- AI 想说"应该" / "大概" / "可能"�?- AI 准备调用实现技能但未检查设计时
- AI 声称"测试通过"但未运行测试命令�?**1% 规则**：如果你认为�?1% 的可能性某个技能适用�?*必须调用**。如果最终发现不适用，你可以不使用它。但跳过检查本身就是违规�?**技能优先级**：流程技能（spec-driven、planning、debugging）先于实现技能（frontend-design、api-design）�?---

### 多阶段任务处�?如果任务跨越多个阶段，按顺序加载�?**示例**：新功能开�?```
1. spec-driven-development �?定义规格
2. planning-and-task-breakdown �?拆解任务
3. incremental-implementation �?逐片实现
4. test-driven-development �?编写测试
5. code-review �?代码审查
6. git-workflow-and-versioning �?提交代码
```

### 阶段检测失�?如果无法确定阶段，询问用户：

> "这个任务处于哪个开发阶段？
> - 需求澄清（还不清楚要做什么）
> - 规格定义（已有概念，需要详细规格）
> - 代码实现（规格已定，开始编码）
> - 测试编写（代码已写，需要测试）
> - 代码审查（测试通过，需要审查）
> - 部署发布（审查完成，准备上线�?

---

## Step 0.5: 设计门控（v12.1 新增，P0�?> 来源：Superpowers brainstorming �?HARD-GATE 设计
> 核心原则�?*设计未批准，不写代码�?* 无论任务多简单�?### 铁律

```
NO CODE BEFORE DESIGN APPROVAL
```

如果任务涉及**创建新功能、修改现有行为、构建组�?*，必须先完成设计审批，才能进入编码阶段�?### 门控流程

```
Step 0: 阶段检测完�?    �?    检测：任务是否涉及创建/修改功能�?    �?    ├─ 否（纯查�?阅读/调试现有代码）→ 跳过门控，继�?    └─ 是（新功�?行为修改/组件构建�?         �?    强制加载 brainstorming skill
         �?    读取: read D:\Users\yindb2\.openclaw\skill-archive\_inactive\brainstorming\SKILL.md
         �?    执行 brainstorming 流程�?    1. 探索项目上下�?    2. 逐一澄清问题（目�?约束/成功标准�?    3. 提出 2-3 个方�?+ 权衡
    4. 展示设计，等待用户批�?         �?    用户批准�?    ├─ �?�?修订设计，重新展�?    └─ �?�?记录设计决策 �?进入编码阶段
```

### 触发条件（满足任一即触发）

| 关键�?| 示例 |
|--------|------|
| 实现/开�?创建 | "实现用户登录功能" |
| 添加/新增 | "添加一个配置面�? |
| 修改行为 | "把这里的逻辑改成..." |
| 构建/搭建 | "搭建一�?API 服务" |
| 重构 | "重构这个模块" |

### 跳过条件（全部满足才跳过�?- 任务纯粹�?*阅读/查询/分析**（不涉及文件修改�?- 任务是对**已有设计**�?bug 修复（设计已存在�?- 用户显式�?直接写，不需要设�?

### 设计审批记录

设计批准后，记录�?`.superpowers/design-approval.md`�?```markdown
# Design Approval
Date: YYYY-MM-DD HH:MM
Task: {任务描述}
Design: {设计摘要}
Status: APPROVED
User confirmed: "yes" / "approved" / "go ahead"
```

### 反模式警�?以下思维 = 你正在合理化跳过设计门控�?| 你的想法 | 现实 |
|---------|------|
| "这太简单了，不需要设�? | 简单项目正是未经审视假设最浪费时间的地方。|
| "我知道用户想要什�? | 知道 �?确认。展示设计，获得批准。|
| "设计会拖慢速度" | 返工更慢。|
| "只是个小改动" | 小改动也可能破坏现有行为。确认设计。|
| "用户很急，先写再说" | 写错了更急。|

### �?brainstorming skill 的关�?- coding-framework Step 0.5 �?*门控**（决定是否需要设计审批）
- brainstorming skill �?*流程**（如何完成设计审批）
- Step 0.5 检测到需要设�?�?读取 `D:\Users\yindb2\.openclaw\skill-archive\_inactive\brainstorming\SKILL.md` 按其流程执行
- brainstorming 完成�?�?回到 coding-framework 继续编码阶段

---

## 技能加载流�?Step 0 检测到阶段 �?读取对应 skill �?SKILL.md �?执行流程 �?回到 coding-framework 继续下一阶段�?
### 🔴 子技能路径映射（铁律：必须使用绝对路径）

| 子技能名�?| 绝对路径 |
|-----------|---------|
| brainstorming | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\brainstorming\SKILL.md` |
| spec-driven-development | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\spec-driven-development\SKILL.md` |
| planning-and-task-breakdown | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\planning-and-task-breakdown\SKILL.md` |
| incremental-implementation | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\incremental-implementation\SKILL.md` |
| api-and-interface-design | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\api-and-interface-design\SKILL.md` |
| context-engineering | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\context-engineering\SKILL.md` |
| source-driven-development | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\source-driven-development\SKILL.md` |
| doubt-driven-development | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\doubt-driven-development\SKILL.md` |
| test-driven-development | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\test-driven-development\SKILL.md` |
| browser-testing-with-devtools | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\browser-testing-with-devtools\SKILL.md` |
| debugging-and-error-recovery | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\debugging-and-error-recovery\SKILL.md` |
| code-review | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\code-review\SKILL.md` |
| code-simplifier | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\code-simplifier\SKILL.md` |
| security-and-hardening | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\security-and-hardening\SKILL.md` |
| performance-optimization | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\performance-optimization\SKILL.md` |
| git-workflow-and-versioning | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\git-workflow-and-versioning\SKILL.md` |
| ci-cd-and-automation | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\ci-cd-and-automation\SKILL.md` |
| deprecation-and-migration | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\deprecation-and-migration\SKILL.md` |
| documentation-and-adrs | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\documentation-and-adrs\SKILL.md` |
| observability-and-instrumentation | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\observability-and-instrumentation\SKILL.md` |
| shipping-and-launch | `D:\Users\yindb2\.openclaw\skill-archive\_inactive\shipping-and-launch\SKILL.md` |

**调用方式**�?```
Step 0 检测到阶段 �?从上方映射表查找路径 �?read {绝对路径} �?按流程执�?�?回到 coding-framework
```

**注意**�?- `code-review` 是入口skill，在 `workspace/skills/` �?- 其他子技能均�?`skill-archive/_inactive/` �?- **禁止使用相对路径**，必须使用绝对路�?
## Karpathy 四原则（v11.5 新增�?> 来源：Andrej Karpathy（前 Tesla AI 总监）对 LLM 编码缺陷的观�?### 原则 1：编码前思考（Think Before Coding�?**不要假设，不要隐藏困惑，呈现权衡�?*

编码前必须：
- **明确陈述假设** �?如果不确定，先问而不是猜
- **呈现多种解读** �?存在歧义时不要默默选一�?- **推回当有理由�?* �?如果有更简单的方案，说出来
- **困惑时停�?* �?说清楚什么不清楚，然后问

### 原则 2：简洁优先（Simplicity First�?**解决问题的最少代码，不做推测性实现�?*

- 不添加未被要求的功能
- 单次使用的代码不做抽�?- 不做未被要求的灵活�?可配置�?- 不为不可能的场景做错误处�?- 200 行能�?50 行解�?�?重写

**检验标�?*：一个资深工程师会说"这太复杂�?吗？如果是，简化�?### 原则 3：精准修改（Surgical Changes�?**只动必须动的。只清理自己造成的混乱�?*

编辑现有代码时：
- 不要"改进"相邻的代码、注释或格式
- 不要重构没坏的东�?- 匹配现有风格，即使你会用不同方式
- 发现无关的死代码 �?提一下，不要�?当你的修改造成孤儿时：
- 删除**你的修改**导致的未使用 import/变量/函数
- 不要删除预先存在的死代码，除非被要求

**检验标�?*：每一行改动都应该能直接追溯到用户的请求�?### 原则 4：目标驱动执行（Goal-Driven Execution�?**定义成功标准。循环直到验证通过�?*

将命令式任务转化为可验证目标�?| 不要�?.. | 而是... |
|-----------|---------|
| "添加验证" | "为无效输入写测试，然后让测试通过" |
| "修复 bug" | "写一个复�?bug 的测试，然后让测试通过" |
| "重构 X" | "确保重构前后测试都通过" |

多步骤任务，陈述简要计划：
1. [步骤] �?验证：[检查点]
2. [步骤] �?验证：[检查点]
3. [步骤] �?验证：[检查点]

**强成功标准让 LLM 能独立循环。弱标准 = 让它能用"）需要不断澄清�?*

### 四原则生效的标志

- diff 中更少的不必要改�?�?只有被要求的改动出现
- 更少因过度复杂导致的重写 �?第一次就写简�?- 澄清问题在实现之�?�?而不是在犯错之后
- 干净、最小化�?PR �?没有顺手重构/"改进"

---

## 原则 5：Agent Brief 持久性（v12.3 新增�?> 来源：Matt Pocock �?triage skill �?"持久性优于精确性——不引用文件路径/行号，只描述行为"
> 原因：spec 不会因为代码重构而失效，行为描述比路径引用更稳定�?### 铁律

**生成�?task spec、任务描述、计划文件中，禁止引用具体文件路径和行号，只描述行为�?*

### 规则

1. **禁止** 在任务描述中引用具体文件路径（如 `src/components/Button.tsx`�?2. **禁止** 在任务描述中引用具体行号（如 `�?2行`�?3. **改为** 描述行为（如"用户登录按钮组件"�?处理支付的函�?�?### 示例对比

| �?错误（路径引用） | �?正确（行为描述） |
|---|---|
| `修复 src/api/user.py �?7行的空指针异常` | `修复用户API中处理空用户ID时的空指针异常` |
| `�?components/Header.tsx 中添加导航菜单` | `在页面顶部导航区域添加菜单组件` |
| `修改 utils/auth.js �?validateToken 函数` | `修改令牌验证函数，增加过期时间检查` |

### 适用范围

- Plan Mode（模�?）生成的 plan.md
- PDD .specs/ 中的 requirements.md、design.md、implementation-plan.md
- DAG 任务�?task description
- spawn 子代理时传入�?task 描述
- 所有委派给子代理的任务 brief

### 例外

- 对话中用户明确要求看某个文件时，可以引用路径
- 代码注释中可以引用路径（�?`// see src/config/routes.ts`�?- **任务描述/spec/计划**中始终用行为描述

### 为什么有效？
- 代码重构后，文件路径会变，但行为不变
- 子代理自行定位文件，比硬编码路径更鲁�?- spec 的寿命远超单次实�?---

## 工作模式

### 模式 1：快速编码（v11.0 增强�?触发：用户要求写代码

流程�?1. 应用 Ponytail 决策阶梯�? 级）
2. 选择最简方案
3. **强制验证循环**（v10.6 新增）：
   - 生成代码后立即执行编�?运行验证
   - 若失败，根据错误信息修复并重新验�?   - 最�?3 次循环，仍失败则报告用户
4. **🦆 自审（Rubber Duck Self-Review�?*（v10.9 新增，v11.3 增强，v11.5 加入 Karpathy 精准修改）：
   - 输出代码前，逐行扫描以下 5 个维度：
     - **安全**：eval/exec/SQL拼接/硬编码凭�?路径遍历
     - **逻辑**：边界条件（空列�?None/0/负数）、类型不匹配、未定义变量
     - **正确�?*：是否真正实现了需求（不是"看起来对"但逻辑偏移�?     - **清晰�?*（v11.3，借鉴 Anthropic Code Simplifier）：
       - 嵌套复杂度：>2层嵌�?�?考虑提前返回或提取函�?       - 命名一致性：变量/函数名是否清晰表达意�?       - 冗余注释：删除描�?代码做什�?的注释（代码本身应该说明�?       - 避免嵌套三元：`a ? b : c ? d : e` �?改用 if/else �?switch
       - 避免过度紧凑：一行代�?> 80字符且含多个操作 �?拆分
     - **精准修改**（v11.5，借鉴 Karpathy Surgical Changes）：
       - 每行改动都能追溯到用户请求吗�?       - 是否"改进"了相邻的代码/注释/格式？→ 不要
       - 是否重构了没坏的东西？→ 不要
       - 是否匹配了现有风格？
       - 你的修改造成的孤儿（未使用import/变量）→ 清理
       - 预先存在的死代码 �?提一下，不要�?   - 发现问题 �?修复后再输出
   - 无问�?�?直接输出
   - ⚠️ 这是"内心独白"式审查，�?spawn 子代理，零额外开销
   - ⚠️ 清晰度检查不追求"更少行数"，而是"更易�?
5. **🧪 TDD 模式检�?*（v11.0 新增）：
   - 如果用户指定 `--strict-tdd` 或任务复杂度 �?medium�?     - 先写测试（red）：`python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\tdd_runner.py red tests/test_xxx.py`
     - 再写实现（green）：`python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\tdd_runner.py green tests/test_xxx.py`
     - 重构（refactor�?     - 运行严格检查：`python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\tdd_runner.py strict --check`
   - 如果检测到代码先于测试 �?删除代码，从测试重新开�?   - ⚠️ 简单任务（trivial/small）可跳过 TDD
6. **🔍 自动代码审查**（v11.2 新增，v11.7 升级为两阶段审查）：
   - 代码编写完成并通过验证后，自动调用 `code-review` skill 进行审查
   - **两阶段审查机�?*（v11.7，借鉴 Superpowers）：
     - **Stage 1: 任务级审�?*（每个任务完成后�?       - 输入：diff + 任务 brief + 全局约束
       - 独立审查子代理，**不信任实现者报�?*
       - 检查：规格合规（Missing/Extra/Misunderstood）、代码质�?       - 发现 Critical/Important �?派发修复子代�?�?重新审查
     - **Stage 2: 分支级审�?*（所有任务完成后，合并前�?       - 输入：整个分�?diff + 计划/规格
       - 检查：跨任务一致�?+ 整体架构 + 生产就绪�?       - 输出：准备合并？[Yes | No | With fixes]
   - 根据任务复杂度自动选择审查深度�?     - trivial / small �?跳过（步�?的🦆自审已覆盖�?     - medium �?Stage 1 任务级审查（独立子代理）
     - large �?Stage 1 + Stage 2 两阶段审�?   - 用户显式�?不需要审�? / `--skip-review` �?跳过
   - **调用方式**：`read D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\code-review\SKILL.md` �?按其流程执行
   - **审查模板**：`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\code-review\templates\task-reviewer-prompt.md` �?`branch-reviewer-prompt.md`
7. **�?完成验证门控**（v12.1 新增，P1，融�?Step 8 Verification Before Completion）：
   - **铁律：没有新鲜验证证据，不能声称完成�?*
   - 在声称任务完成之前，必须执行该任务类型对应的验证命令�?     - 代码实现 �?运行测试/lint/build（`pytest` / `npm test` / `cargo test`�?     - 文档编写 �?检查渲染效果、链接有效�?     - 配置修改 �?服务重启验证、配置语法检�?   - 验证流程�? 步）�?     1. **IDENTIFY**：什么命令能证明这个声明�?     2. **RUN**：执行完整命令（fresh, complete�?     3. **READ**：完整输出，检�?exit code，统计失败数
     4. **VERIFY**：输出是否确认了声明�?     5. **ONLY THEN**：做出声�?+ 附上证据
   - 禁止的表达：
     - �?"应该能过" �?�?[运行命令] [看到: 34/34 pass] "全部通过"
     - �?"看起来没问题" �?�?[运行lint] [看到: 0 errors] "lint通过"
     - �?"我很有信�? �?�?信心 �?证据。运行验证�?   - Red Flags（出现以下想�?�?STOP，先运行验证）：
     - "应该能过" / "看起来没问题" / "我很有信�?
     - "Agent 说成功了" / "部分检查就够了"
8. 输出格式：`[code] �?skipped: [X], add when [Y]`
9. **📋 任务追踪**（v11.9 新增，借鉴 snarktank/ralph）：
   - 任务开始时创建 `tasks/task-{id}.json`（从模板复制�?   - 每完成一�?story，更�?`passes: true` + `completed_at`
   - 所�?story 完成 �?任务状态变�?`done`
   - 任务完成后触发归档（�?自动归档机制"�?   - **模板位置**：`tasks/task-template.json`
   - **前端任务强制规则**（v11.9）：acceptance_criteria 必须包含浏览器验证步�?**强制验证规则**（v10.6 新增）：
- Python：`python -m py_compile <file>` �?`python <file>`
- JavaScript/TypeScript：`node --check <file>` �?`tsc --noEmit`
- Bash：`bash -n <file>`
- 其他语言：使用对应编译器/解释器验�?- 验证失败时，将完整错误信息传回模型修�?**Backpressure 三层门控**（v11.4 新增，借鉴 ralph-orchestrator）：

代码通过编译验证后，自动运行门控检查：

```
代码生成 �?Gate 1（编译）�?Gate 2（测试）�?Gate 3（质量）�?输出
              │失�?         │失�?        │失�?           自动修复         自动修复       报告用户
```

| 门控 | 触发条件 | 检查内�?| 失败处理 |
|------|---------|---------|---------|
| Gate 1: 编译 | 始终运行 | py_compile / node --check / tsc | 自动修复3�?|
| Gate 2: 测试 | 复杂�?�?medium 且有测试 | pytest / npm test | 自动修复3�?|
| Gate 3: 质量 | 项目已配�?lint/typecheck | ruff / eslint / mypy / tsc --noEmit | lint 自动修复，typecheck 报告用户 |

**执行方式**�?```bash
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py gates --files "src/main.py,src/utils.py" --complexity medium
```

**跳过条件**：trivial/small 复杂度、项目无测试/lint 配置、用�?`--skip-gates`

### 任务追踪机制（v11.9 新增，借鉴 snarktank/ralph�?**目的**：结构化追踪任务进度，支持断点续做和历史归档�?**文件结构**�?```
tasks/
├── task-template.json    # 模板
├── task-001.json         # 具体任务
└── task-002.json
```

**task.json 格式**�?```json
{
  "id": "task-001",
  "title": "集成 Firecrawl 云服�?,
  "branch": "feature/firecrawl-integration",
  "created": "2026-07-08T10:00:00Z",
  "status": "done",
  "passes": true,
  "stories": [
    {
      "id": "story-1",
      "title": "创建 firecrawl skill",
      "passes": true,
      "acceptance_criteria": ["SKILL.md 完整", "测试 3/3 通过", "已提�?],
      "completed_at": "2026-07-08T10:30:00Z"
    }
  ],
  "learnings": ["firecrawl-py API 与文档不完全一�?],
  "archived": false
}
```

**状态流�?*�?```
pending �?in-progress �?done
              �?              blocked（需要外部输入）
```

**触发规则**�?- 任务涉及 3+ 个文件修�?�?创建 task.json
- 任务涉及多步�?�?每个步骤一�?story
- 前端任务 �?acceptance_criteria 必须包含 "Verify in browser"

### 自动归档机制（v11.9 新增，借鉴 snarktank/ralph�?**目的**：保留任务执行历史，支持复盘和知识积累�?**归档触发条件**�?- task.json 状态变�?`done`
- 所�?story �?`passes: true`
- 代码已提交到 git

**归档目录结构**�?```
archive/
└── YYYY-MM-DD-feature-name/
    ├── task.json          # 任务定义（从 tasks/ 复制�?    ├── execution.log      # 执行日志（从对话提取�?    ├── learnings.md       # 学习记录（从 .learnings/ 提取�?    └── changes.md         # 代码变更摘要（从 git log 提取�?```

**归档流程**�?1. 创建归档目录：`archive/YYYY-MM-DD-{branch-name}/`
2. 复制 task.json 到归档目�?3. 生成 changes.md：`git log --oneline {branch}..main`
4. 提取 learnings：从 `.learnings/` 复制相关文件
5. 更新 task.json：`archived: true`, `archived_at: timestamp`
6. �?`tasks/` 删除原文件（可选，保留则不删除�?### 浏览器验证强制化（v11.9 新增，借鉴 snarktank/ralph�?**规则**：前端任务的 acceptance_criteria 必须包含浏览器验证步骤�?**检测条�?*（满足任一即视为前端任务）�?- 修改�?`.tsx/.jsx/.vue/.html/.css/.scss` 文件
- 修改�?`src/components/` �?`src/pages/` 目录
- 任务描述包含"UI"/"前端"/"页面"/"组件"

**强制添加的验收标�?*�?```json
{
  "acceptance_criteria": [
    "...",
    "Verify in browser using browser-testing-with-devtools skill"
  ]
}
```

**执行方式**�?1. 检测到前端任务 �?自动注入浏览器验证步�?2. 代码审查时检�?�?缺少浏览器验�?�?标记�?Critical
3. 执行浏览器验�?�?使用 `browser-testing-with-devtools` skill

---

### 模式 2：代理审�?触发：用户要求审查代�?/ "review"

流程�?1. 根据代码特征选择代理�?-7 个）
2. 并行 spawn 子代理执行审�?3. 按严重度分级阈值过滤发�?4. 合并去重，汇总为统一审查报告

**置信度分级阈�?*（v10.1 改进）：

| 严重�?| 置信度阈�?| 说明 |
|--------|------------|------|
| Critical | �?50 | 安全漏洞、数据丢失风险，低阈值确保不漏报 |
| High | �?70 | 逻辑错误、性能问题 |
| Medium | �?80 | 代码风格、最佳实�?|
| Low | �?90 | 风格建议、可选优化，高阈值避免噪�?|

**合并策略**（v10.1 新增）：
- 按文�?行号归组
- 同一位置多个代理报告 �?严重度取最�?- 合并建议文本，标记来源代�?- 冲突报告（同一位置不同结论）→ 保留两者，标记"需人工判断"

### 模式 3：迭代改�?触发：用户要求优�?/ "iterate" / 性能问题

流程�?1. 初始化迭代状态（loop-controller.py init�?2. 分析 �?改进 �?验证 �?循环
3. 完成条件满足 �?退出（loop-controller.py complete�?### 模式 4：安全守�?触发：exec 命令执行�?流程�?1. PreExec 检查（25 种安全模式）
2. 匹配 critical/high �?阻止 + 报告
3. 匹配 medium �?允许 + 记录
4. PostExec 日志

## 决策�?```
用户请求
    �?    ├─ 写代�?�?模式 1（快速编码）
    �?  ├─ 简单任�?�?直接�?    �?  └─ 复杂任务 �?spawn coding-agent
    �?  ├─ 完成�?�?🔍 两阶段代码审查（v11.8，借鉴 Superpowers�?    �?  �?  ├─ trivial/small �?跳过（自审已覆盖�?    �?  �?  ├─ medium �?Stage 1: 任务级审查（独立子代理）
    �?  �?  └─ large �?Stage 1 + Stage 2: 分支级审�?    �?  �?      └─ 不信任实现者报告，对照 diff 验证
    �?  └─ 输出�?�?🚧 Backpressure 门控（v11.4�?    �?      ├─ Gate 1: 编译（始终）
    �?      ├─ Gate 2: 测试（≥medium�?    �?      └─ Gate 3: 质量（已配置时）
    �?    ├─ 审查代码 �?模式 2（代理审查）
    �?  ├─ 小改�?�?单代理（code-reviewer�?    �?  └─ 大改�?�?多代理并�?    �?  └─ 或直接调�?code-review skill（v11.2 推荐�?    �?    ├─ 优化/调试 �?模式 3（迭代改进）
    �?  └─ loop-controller 管理状�?    �?    ├─ 执行命令 �?模式 4（安全守卫）
    �?  └─ hook-engine PreExec 检�?    �?    ├─ 完整开�?�?模式 5（工作流编排�?    �?  └─ 规划→执行→🔍两阶段审查（任务�?分支级）→🚧门控→优化
    �?    ├─ 先做计划 �?模式 6（Plan Mode）（v10.9�?    �?  ├─ trivial~medium �?简�?plan.md
    �?  └─ large/critical �?PDD .specs/ 目录（v11.4�?    �?      └─ requirements.md + design.md + implementation-plan.md
    �?    ├─ 快速侦�?�?模式 7（Explore）（v10.9�?    �?  └─ spawn explore 代理 �?返回结论摘要
    �?    ├─ 迭代循环 �?模式 8（Ralph Loop�?    �?  └─ hook-engine ralph_loop.py 管理迭代
    �?    └─ 自我审查 �?模式 9（三角色切换）（v12.1�?        └─ Implementer �?Reviewer �?Fixer，无需子代�?```

## Ponytail 决策阶梯（编码前必过�?停止在第一个能 hold 住的层级�?1. **这需要存在吗�?* �?推测性需�?= 跳过（YAGNI�?2. **代码库已有？** �?复用 helper/util/type/pattern
3. **标准库能做？** �?用它
4. **平台原生功能�?* �?`<input type="date">` 优于 picker lib，CSS 优于 JS
5. **已安装依赖能解决�?* �?用它，不新增依赖
6. **一行搞定？** �?一�?7. **最小可行实现？** �?最后才写完整代�?### YAGNI 判断标准（v10.1 新增�?**跳过条件**（必须同时满足）�?- 未来需求概�?< 20%
- 实现成本 > 5 行代�?- 跳过不会破坏当前抽象层次

**不跳过（架构性需求白名单�?*�?- 接口定义（interface/type declaration�?- 插件机制入口
- 错误码枚�?- 配置项骨�?
**一行代码限�?*�?- 仅适用于语义清晰、无副作用的纯表达式
- 不超�?80 字符
- 可单步调�?
**输出格式**�?```
[code]
�?skipped: [功能X] (reason: L3 - 标准库已提供) | add when [场景Y] confirmed
```

**不简化的边界**：输入验证（信任边界处）、防数据丢失的错误处理、安全措施、可访问性基础�?**Bug 修复**：修根因，不修症状。grep 所有调用者，在共享函数加 guard�?**标记简�?*：`// ponytail: global lock, per-account locks if throughput matters`

## 安全守卫（exec 前必过）

### 安全检查分层（v10.1 改进�?**命令级安全检�?*（pre-exec-check.sh 负责）：
- 针对 shell 命令（rm、del、format 等）
- 静态字符串匹配 + 正则
- �?exec 执行前拦�?**代码级安全检�?*（security-auditor 代理负责）：
- 针对源代码文件内容（eval、exec、SQL 拼接等）
- 静态代码分�?- 在审查模式中检�?> 注意：`pre-exec-check.sh` 只处理命令级安全检查。代码中�?`eval()`、`exec()` 等风险由 security-auditor 代理在审查模式中处理，而非�?exec 前拦截�?### 25 种安全模式，4 级严重度
| 级别 | 处理方式 |
|------|----------|
| critical | 阻止执行 + 报告用户 + 记录日志 |
| high | 阻止执行 + 请求确认 + 记录日志 |
| medium | 允许执行 + 记录告警日志 |
| low | 记录日志，不干预 |

模式类别：危险命令、注册表操作、账户管理、服务管理、计划任务、外部下载、批量操作、提权操作、敏感数据传输、代码执行风险、敏感信息泄露、路径遍历、SQL 注入、XSS 风险、不安全反序列化、硬编码凭证、不安全加密、资源泄漏、竞态条件、不安全随机数、日志注入、SSRF、XXE、不安全 CORS、依赖漏洞�?详细模式列表：`read D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\security-patterns-detail.md`

## 代码质量保障（v10.6 新增�?### 自检修正入口

**强制规则**：最终输出代码前，必须通过自检�?**自检流程**�?1. 语法验证（编�?解释�?2. 静态分析（如有 linter�?3. 运行测试（如有测试套件）
4. 安全检查（模式 4�?**自检命令**�?```bash
# Python
python -m py_compile <file> && python -m pytest <test_file> -v

# JavaScript/TypeScript
node --check <file> && npm test

# Bash
bash -n <file>
```

**失败处理 �?3-Strike 错误协议**（v11.1 新增）：

```
ATTEMPT 1: Diagnose & Fix
  �?读错误信息，找根�?  �?应用针对性修�?  
ATTEMPT 2: Alternative Approach
  �?同一错误？换方法
  �?换工具？换库�?  �?绝不重复完全相同的失败操�?
ATTEMPT 3: Broader Rethink
  �?质疑假设
  �?搜索解决方案
  �?考虑更新计划

AFTER 3 FAILURES: Escalate to User
  �?解释尝试了什�?  �?分享具体错误
  �?请求指导
```

**核心规则**�?- `if action_failed: next_action != same_action`
- 追踪尝试过的方法，变异策�?- 绝不隐藏错误并静默重�?### 静态分析工具（v10.6 新增�?**脚本**：`scripts/static_analysis.py`

**用法**�?```bash
# 自动检测语言�?linter
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\static_analysis.py src/main.py

# 指定 linter
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\static_analysis.py src/app.js --linter eslint

# JSON 输出（便于自动化�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\static_analysis.py src/main.py --format json

# �?error 级别时退出码 1
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\static_analysis.py src/main.py --fail-on-error
```

**支持�?linter**�?| 语言 | linter | 安装方式 |
|------|--------|----------|
| Python | flake8 | `pip install flake8` |
| Python | pylint | `pip install pylint` |
| JavaScript/TS | eslint | `npm install -g eslint` |
| Bash | shellcheck | 系统包管理器 |

**集成规则**�?- 模式 1（快速编码）：生成代码后自动运行 `static_analysis.py`
- 模式 2（代理审查）：code-reviewer 代理自动调用
- error 级别告警必须修复，warning 需说明忽略原因

### 分层验证栈（v10.6 新增�?**脚本**：`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\layered_validate.py`

**三层定义**�?| �?| 名称 | 检查内�?| 失败处理 |
|----|------|----------|----------|
| L1 | 语法检�?| 编译/解析 | 立即停止，修复语�?|
| L2 | 语义检�?| 类型、导入、作用域 | 停止，修复语�?|
| L3 | 逻辑检�?| 运行测试 | 停止，修复逻辑 |

**用法**�?```bash
# 完整三层验证
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\layered_validate.py src/main.py

# 跳过测试（仅语法+语义�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\layered_validate.py src/main.py --skip-tests

# JSON 输出
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\layered_validate.py src/main.py --format json
```

**强制规则**�?- 任何代码生成后，必须通过 L1+L2 验证
- L3 在有测试文件时强制执�?- 任一层失�?�?修复后重新验�?�?最�?3 次循�?### TDD 流程工具（v10.6 新增�?**脚本**：`scripts/tdd_runner.py`

**TDD 红绿循环**�?```
红灯（Red）→ 绿灯（Green）→ 重构（Refactor�?```

**用法**�?```bash
# 红灯阶段：运行测试，期望失败
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\tdd_runner.py red tests/test_main.py

# 绿灯阶段：运行测试，期望通过
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\tdd_runner.py green tests/test_main.py

# 完整循环
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\tdd_runner.py cycle tests/test_main.py src/main.py
```

**强制规则**（当用户要求 TDD 时）�?1. 先编写测试用�?2. 运行 `tdd_runner.py red` �?确认测试失败（红�?✓）
3. 编写实现代码
4. 运行 `tdd_runner.py green` �?确认测试通过（绿�?✓）
5. 重构代码，保持绿�?### 运行时异常上下文注入（v10.6 新增�?**脚本**：`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\run_with_context.py`

**功能**：运行脚本，捕获异常时收集局部变量快�?+ traceback + 修复建议

**用法**�?```bash
# 运行脚本，异常时输出完整上下�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\run_with_context.py src/main.py

# 带参�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\run_with_context.py src/main.py --arg1 val1
```

**输出内容**�?- 异常类型和消�?- 异常位置（文�?行号:源代码）
- 调用�?- 异常点局部变量快照（类型、值、长度等�?- 异常链（cause/context�?- 修复建议提示

**强制规则**�?- 代码运行失败时，使用 `run_with_context.py` 替代直接运行
- 根据输出的局部变量和修复建议定位根因
- 修复后重新运行验�?### 性能基准对比（v10.8 新增�?**脚本**：`scripts/benchmark_runner.py`

**功能**：对性能敏感函数生成 2+ 种实现方案，自动跑分对比，选择最优解�?**用法**�?```bash
# �?JSON 配置文件运行
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\benchmark_runner.py run config.json

# JSON 输出
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\benchmark_runner.py run config.json --format json

# 覆盖超时
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\benchmark_runner.py run config.json --timeout 60
```

**JSON 配置格式**�?```json
{
  "name": "list_dedup",
  "setup": "import random; data = [random.randint(0, 100) for _ in range(10000)]",
  "snippets": [
    {"name": "dict_from_keys", "code": "list(dict.fromkeys(data))"},
    {"name": "seen_set", "code": "seen = set(); [x for x in data if x not in seen and not seen.add(x)]"}
  ],
  "iterations": 1000,
  "warmup": 10,
  "validate": "assert sorted(r1) == sorted(r2)",
  "edge_cases": [
    {"name": "empty", "setup": "data = []"},
    {"name": "single", "setup": "data = [42]"}
  ],
  "timeout_per_snippet": 30
}
```

**性能指标**�?- **中位�?*（主决策指标，天然抗异常值）
- **P95**（尾部延迟）
- **标准�?*（稳定性判断）
- **内存峰�?*（tracemalloc 估算值）

**三级正确性验�?*�?- V1: 默认 `==` 比较
- V2: 自定�?`validate` 表达式（`r1`, `r2` 代表两个方案输出�?- V3: 边界用例 `edge_cases`（空输入、单元素、极端值）

**触发条件**�?- **AUTO_TRIGGER**: layered_validate L3 测试中执行时�?> 1s
- **SUGGEST**: 用户明确要求性能优化 / 循环 > 1000 �?/ 处理大数据集

**强制规则**�?- 性能敏感函数必须生成至少 2 种实�?- 所有方案必须通过正确性验证（含边界用例）
- 选择中位数最快的方案，除非有明确理由选择其他
- 输出 benchmark 报告供用户确�?**错误处理**�?- `SYNTAX_ERROR`: 代码语法错误，跳过该方案
- `TIMEOUT`: 执行超时�? timeout_per_snippet），跳过
- `OOM`: 内存溢出，跳�?- `VALIDATE_ERROR`: 验证函数本身报错，提示用户检�?**局限�?*�?- tracemalloc 无法跟踪子进程内存，多线程场景统计可能偏�?- v10.8 仅支�?Python，JS/TS 为实验�?- 不提供统计显著性检验（如需精确统计建议使用 pytest-benchmark�?### 依赖影响分析（v10.8 新增�?**脚本**：`scripts/analyze_impact.py`

**功能**：修改模块后，自动分析影响范围，只跑相关测试以加速验证�?**用法**�?```bash
# 分析单个文件
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py src/utils.py

# 限制 BFS 深度（仅直接依赖�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py src/utils.py --depth 1

# 分析 git diff（自动获取修改文件）
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py --git-diff

# 分析并直接运行测�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py --git-diff --run-tests

# JSON 输出
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py src/utils.py --format json

# 指定项目根目�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py src/utils.py --root /path/to/project

# 依赖提取级别（L1=AST, L2=+正则, L3=+文件名）
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\analyze_impact.py src/utils.py --level L2
```

**核心原理**�?- AST 解析 import 构建有向依赖�?- �?*反向依赖**�?BFS（谁依赖�?= 修改后会影响谁）
- 三级测试映射确定受影响测�?**三级测试映射**�?| 级别 | 策略 | 示例 |
|------|------|------|
| M1 精确匹配 | `src/foo/bar.py` �?`tests/**/test_bar.py` | src/utils/parser.py �?tests/test_parser.py |
| M2 目录匹配 | `src/foo/` �?`tests/foo/` | src/utils/ �?tests/utils/ |
| M3 反向依赖 | test_a.py import �?src/utils.py �?受影�?| tests/test_api.py imports utils |
| 兜底 | 找不到对应测�?�?提示全量运行 | �?|

**触发条件**�?- 修改了共享模块（utils、config、types 等）�?自动触发
- 不确定修改是否影响其他模�?�?建议触发

**�?layered_validate 集成**�?- L3 发现修改文件后，自动调用 analyze_impact 给出建议
- **实际执行由用户确�?*（避免虚假安全感�?**强制规则**�?- 修改共享模块后，必须运行 `analyze_impact.py` 确定影响范围
- 只运行受影响的测试，不跑全量测试
- 影响范围超过 10 个测试文件时，先跑直接依赖，再跑间接依赖
- 使用 `--git-diff` 可自动分析当前未提交的修�?**大项目优�?*�?- 依赖图缓存到 `.impact_cache.json`（文件修改时间戳校验，增量更新）
- `--depth N` 控制 BFS 深度（默认全图，不静默截断）
- >1000 文件时显示警告，让用户确认是否限制深�?### 差异对比自审

**触发条件**：修改现有文件后

**强制流程**�?1. 使用 `git diff` 查看变更
2. 自我审视变更合理性：
   - 是否引入了不必要的更改？
   - 是否可能破坏现有功能�?   - 是否符合项目风格�?3. 发现问题 �?修正后再输出

**示例**�?```bash
git diff src/main.py
```

**审视清单**�?- [ ] 变更是否最小化（只改必要的）？
- [ ] 是否保留了原有功能？
- [ ] 是否遵循项目编码规范�?- [ ] 是否有遗漏的边界情况�?## 代理系统

7 个专业代理，按需选择�?| 代理 | 职责 | 触发场景 |
|------|------|----------|
| code-reviewer | 代码质量 + YAGNI 检�?| "审查代码" / "review" |
| security-auditor | 漏洞 + 凭证 + CWE | "安全检�? / "漏洞" |
| test-engineer | 覆盖�?+ 用例生成 | "写测�? / "覆盖�? |
| architecture-critic | 模块 + 依赖 + 扩展�?| "架构审查" / "模块设计" |
| performance-analyst | 复杂�?+ 资源 + 并发 | "性能审查" / "瓶颈" |
| maintainability-reviewer | 命名 + 复杂�?+ 债务 | "可维护�? / "技术债务" |
| documentation-checker | API 文档 + 注释 | "文档检�? / "注释" |

### 代理职责矩阵（v10.1 新增�?避免重复审查，各代理独占检查项目：
| 检查项 | 主责代理 | 协助代理 |
|--------|----------|----------|
| 代码风格/命名 | code-reviewer | maintainability-reviewer |
| 逻辑正确�?| code-reviewer | - |
| 安全漏洞/CWE | security-auditor | - |
| 硬编码凭�?| security-auditor | code-reviewer |
| 测试覆盖�?| test-engineer | - |
| 模块耦合�?| architecture-critic | maintainability-reviewer |
| 算法复杂�?| performance-analyst | - |
| 技术债务评估 | maintainability-reviewer | architecture-critic |
| API 文档完整�?| documentation-checker | - |

**分层过滤**（v10.1 改进）：
- 先快速扫描安�?critical 问题
- 若发�?�?立即中断并通知用户，不必等其他代理完成
- 若无 �?继续完整审查流程

详细代理定义：`read D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\agents\*.yaml`

### 语言专属审查（v10.3 新增�?审查代码时，系统会根据文件扩展名自动选择语言专属 reviewer�?| 扩展�?| 专属 Reviewer | 审查重点 |
|--------|---------------|----------|
| .py | python-reviewer | PEP 8、类型注解、Pythonic 惯用法、安�?|
| .ts/.tsx/.js/.jsx | typescript-reviewer | 类型安全、React 最佳实践、异步处�?|
| .go | go-reviewer | goroutine、channel、错误处�?|
| .rs | rust-reviewer | 所有权、生命周期、unsafe |

**语言路由规则**�?- `review-orchestrator.py --auto-select` 自动检测文件扩展名
- 语言专属 reviewer 与通用 code-reviewer 并行工作
- 审查报告合并输出，按文件+行号归组

**示例**�?```bash
# 审查 Python 代码，自动选择 python-reviewer + code-reviewer
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\review-orchestrator.py \
  --files "src/main.py" \
  --auto-select
```

## 🔍 自动代码审查集成（v11.2 新增�?> 借鉴 Anthropic 官方 Code Review Plugin 设计，编码完成后自动触发多代理并行审查�?### 集成架构

```
coding-framework（编码）
    �?    ├─ 步骤1-5: 编码 + 验证 + 自审
    �?    └─ 步骤6: 自动调用 code-review skill
         �?         ├─ trivial/small �?跳过（🦆自审已覆盖�?         ├─ medium �?快速审查（1代理，Bug Hunter视角�?         ├─ large �?标准审查�?代理并行：Bug + Security + Maintainability�?         └─ 关键模块 �?深度审查�?代理并行 + History + Spec Compliance�?              �?              ├─ 发现 high/critical �?修复 �?重新审查
              └─ 无高置信度问�?�?输出代码
```

### �?code-review skill 的关�?| 场景 | 触发方式 | 审查深度 |
|------|---------|---------|
| 写完代码后自动审�?| coding-framework 模式1步骤6自动触发 | 按复杂度分层 |
| 用户主动要求审查 | 用户�?审查代码" �?直接调用 code-review skill | 用户指定或默认标�?|
| 完整开发流程中的审�?| coding-framework 模式5审查阶段自动触发 | 按任务复杂度 |
| DAG 任务中的审查 | DAG review 阶段自动触发 | 按任务复杂度 |

### 调用方式

```
# 自动触发（无需用户干预�?代码编写完成 �?验证通过 �?自动 read D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\code-review\SKILL.md �?按流程执�?
# 手动触发
用户�?审查这段代码" �?直接 read D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\code-review\SKILL.md �?按流程执�?
# 跳过审查
用户�?不需要审�? / --skip-review �?跳过步骤6
```

### 审查深度选择逻辑

```python
def select_review_depth(task_complexity, is_critical_module):
    if task_complexity in ('trivial', 'small'):
        return None  # 跳过，🦆自审已覆盖
    elif task_complexity == 'medium':
        return 'quick'  # 快速审查，1代理，~30�?    elif task_complexity == 'large':
        if is_critical_module:
            return 'deep'  # 深度审查�?代理�?-5分钟
        else:
            return 'standard'  # 标准审查�?代理�?-2分钟
```

### 关键模块识别

以下情况视为"关键模块"，自动升级为深度审查�?- 涉及认证/授权/加密
- 涉及数据库操作（CRUD核心逻辑�?- 涉及外部API调用
- 涉及并发/多线�?- 修改共享模块（utils、config、types�?- 安全敏感（处理用户输入、文件操作）

## 迭代循环

3 种模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| fixed | 固定次数 | 已知需�?N �?|
| max | 最大次�?+ 完成条件 | 有明确完成标�?|
| adaptive | 根据改进幅度动态调�?| 不确定需要多少轮 |

### 自适应模式度量标准（v10.1 新增�?**强制要求**：使�?adaptive 模式时，必须设置至少一个可度量指标�?- 响应时间（p50/p95/p99�?- 内存峰�?- 代码行数减少比例
- 测试通过�?- 自定义指标（通过 regex 提取�?**度量方式**�?```bash
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py init \
  --name "性能优化" \
  --mode adaptive \
  --metric "response_time_p95" \
  --threshold "0.1"  # 改进幅度 < 10% 时停�?```

**回退规则**：若用户未提供可度量指标，自动回退�?max 模式并提示�?### 完成条件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| regex | 正则匹配输出 | `--condition "regex:All tests passed"` |
| file | 文件存在 | `--condition "file:output/result.json"` |
| file-changed | 文件内容变化 | `--condition "file-changed:src/main.py"` |
| llm | LLM 判断（v10.1 规范化） | 封闭性问�?+ JSON 布尔值返�?|

**LLM 完成条件规范**（v10.1 新增）：
- 必须基于封闭性问题（�?代码是否通过所有测试？"�?- 返回格式：`{"complete": true/false, "reason": "..."}`
- 禁止开放式问题（如"代码是否足够好？"�?控制器：`python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py init --name "task" --mode max --max 10`

### 反事实解释修复法（v10.6 新增�?**触发条件**：同一错误连续修复失败 2 次�?**强制流程**�?1. 停止自动修复
2. 输出自然语言解释�?   ```
   我认为之前的修复无效是因为：
   - �?1 次修复尝试：[描述] - 失败原因：[分析]
   - �?2 次修复尝试：[描述] - 失败原因：[分析]
   - 根本原因可能是：[推断]
   ```
3. 基于该解释生成新的修复方�?4. 验证新方�?**目的**：避免盲目试错，强制模型理解错误根因后再修复�?**示例**�?```
错误：IndexError: list index out of range

�?1 次尝试：添加边界检�?if i < len(lst)
失败原因：检查位置错误，在访问后才检�?�?2 次尝试：在访问前添加 try-except
失败原因：异常被吞掉，未处理根本问题

根本原因：列表为空时不应进入循环，需检查列表是否为�?```

### De-Sloppify 清理轮次（v10.3 新增�?LLM 编码常产�?冗余代码"（测试语言特性、过度防御、console.log 等）。De-Sloppify 模式在实现轮次之间插入清理轮次，保持代码简洁�?**执行顺序**（interval=2 为例）：
```
iter 1: 实现功能
iter 2: 实现功能
iter 3: 清理轮次（de-sloppify�?iter 4: 实现功能
iter 5: 实现功能
iter 6: 清理轮次
...
```

**使用方法**�?```bash
# 启用 De-Sloppify
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py init \
  --name "功能开�? \
  --mode max --max 9 \
  --sloppify \
  --sloppify-interval 2
```

**清理轮次聚焦**�?- 删除类型系统已保证的冗余运行时检�?- 删除过度防御性的错误处理
- 删除 console.log / 注释掉的代码
- 删除未使用的导入和变�?- 简化冗余的条件判断

**check 命令输出**�?```json
{
  "action": "check",
  "should_continue": true,
  "iteration": 2,
  "is_sloppify_round": true,
  "sloppify_focus": [
    "删除未使用的导入和变�?,
    "删除 console.log / 注释掉的代码",
    "..."
  ]
}
```

## 审查编排

多代理并行审查使用编排脚本：

```bash
# 基本用法
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\review-orchestrator.py \
  --files "src/main.py" \
  --agents "code-reviewer,security-auditor"

# 自动选择代理 + JSON 输出（v10.1�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\review-orchestrator.py \
  --files "src/main.py" \
  --auto-select \
  --output json

# 分层过滤：先扫描安全 critical（v10.1�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\review-orchestrator.py \
  --files "src/" \
  --fast-fail  # 发现 critical 立即中断
```

**输出格式**（v10.1 改进）：
- 默认：人类可读的 Markdown 报告
- `--output json`：结构化 JSON，便于自动化集成

## Hook 系统

事件类型�?| 事件 | 触发时机 |
|------|----------|
| PreExec | exec 命令执行�?|
| PostExec | exec 命令执行�?|
| Stop | 会话结束前（迭代循环用） |

Hook 脚本位于 `hooks/` 目录，从 stdin 读取 JSON 事件数据，输�?JSON 决策�?## 渐进式披�?核心指令�?SKILL.md（本文件），详细参考按需加载�?- Hook 系统详情 �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\hook-system.md`
- 代理系统详情 �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\agent-system.md`
- 迭代模式详情 �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\iteration-patterns.md`
- 安全模式详情 �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\security-patterns-detail.md`
- 工作流示�?�?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\workflow-examples.md`
- **外部代理委派** �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\external-agents.md`（Codex/Claude Code/Git Worktree 并行�?## 文件结构

```
coding-framework/
├── SKILL.md                          # 本文件（编排器）
├── .coding-framework.yml             # 配置文件（v10.1 新增�?├── CONTRIBUTING.md                   # 扩展指南（v10.1 新增�?├── agents/                           # 8 个子代理定义（v10.9 新增 explore�?�?  ├── code-reviewer.yaml
�?  ├── security-auditor.yaml
�?  ├── test-engineer.yaml
�?  ├── architecture-critic.yaml
�?  ├── performance-analyst.yaml
�?  ├── maintainability-reviewer.yaml
�?  ├── documentation-checker.yaml
�?  └── explore.yaml                  # 侦察代理（v10.9 新增�?├── hooks/                            # 3 个钩子脚�?�?  ├── pre-exec-check.sh
�?  ├── post-exec-log.sh
�?  └── stop-iteration.sh
├── rules/                            # 4 个规则文�?�?  ├── security-rules.md
�?  ├── security-patterns.md
�?  ├── coding-standards.md
�?  └── review-checklist.md
├── scripts/                          # 9 个工具脚�?�?  ├── loop-controller.py
�?  ├── review-orchestrator.py
�?  ├── check-environment.py          # 环境检查（v10.2 新增�?�?  ├── static_analysis.py            # 静态分析（v10.7 新增�?�?  ├── layered_validate.py           # 分层验证栈（v10.7 新增�?�?  ├── tdd_runner.py                 # TDD 流程（v10.7 新增�?�?  ├── run_with_context.py           # 异常上下文注入（v10.7 新增�?�?  ├── benchmark_runner.py           # 性能基准对比（v10.8 新增�?�?  ├── analyze_impact.py             # 依赖影响分析（v10.8 新增�?�?  └── worktree-manager.py           # Git Worktree 管理（v11.0 新增�?├── plans/                            # Plan Mode 计划文件（v10.9 新增�?�?  └── README.md
└── references/                       # 6 个参考文�?    ├── hook-system.md
    ├── agent-system.md
    ├── iteration-patterns.md
    ├── security-patterns-detail.md
    ├── workflow-examples.md
    ├── external-agents.md
    └── worktree-guide.md             # Git Worktree 使用指南（v11.0 新增�?```

## 配置（v10.1 新增�?通过 `.coding-framework.yml` 自定义行为：

```yaml
# 安全规则
security:
  enabled: true
  fast_fail: true  # 发现 critical 立即中断

# 代理配置
agents:
  default_model: sonnet
  confidence_thresholds:
    critical: 50
    high: 70
    medium: 80
    low: 90

# 迭代循环
iteration:
  default_mode: max
  heartbeat_timeout: 300  # �?
# 日志
logging:
  level: info  # debug/info/warn/error
  format: jsonl
  path: .coding-framework/logs/
```

## 扩展机制（v10.1 新增�?**新增代理**�?1. �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\agents\` 下创�?`your-agent.yaml`
2. �?`.coding-framework.yml` 中注�?3. 详见 `CONTRIBUTING.md`

**新增安全模式**�?1. �?`rules/security-patterns.md` 中添加模式定�?2. �?`rules/security-rules.md` 中添加匹配规�?3. pre-exec-check.sh 自动加载

**新增迭代模式**�?1. �?`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py` 中添加模式处理逻辑
2. 更新 `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\iteration-patterns.md`

## 文档加载决策表（v10.2 新增�?根据用户输入关键词自动预加载对应参考文档：

| 关键�?| 预加载文�?| 说明 |
|--------|------------|------|
| 安全、漏洞、hook、pre-exec | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\security-patterns-detail.md` | 安全模式详情 |
| 代理、审查、review、agent | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\agent-system.md` | 代理系统说明 |
| 迭代、循环、loop、iterate | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\iteration-patterns.md` | 迭代模式说明 |
| Codex、Claude Code、worktree | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\external-agents.md` | 外部代理委派 |
| 示例、workflow、怎么�?| `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\workflow-examples.md` | 工作流示�?|
| hook 事件、stdin、JSON | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\references\hook-system.md` | Hook 系统说明 |

**加载规则**�?- 匹配到关键词时，自动 `read` 对应文档的前 100 行作为上下文
- 多个关键词匹配时，按优先级加载（安全 > 代理 > 迭代 > 外部 > 示例 > hook�?- 最多预加载 2 个文档，避免 token 浪费

## 依赖与环境要求（v10.2 新增�?### 必需依赖

| 依赖 | 版本 | 用�?| 安装方式 |
|------|------|------|----------|
| Python | 3.10+ | loop-controller.py, review-orchestrator.py | 系统包管理器 |
| Git | 2.28+ | worktree 并行、版本控�?| 系统包管理器 |
| bash | 4.0+ | hook 脚本执行 | Git Bash (Windows) / 系统自带 |

### 可选依�?| 依赖 | 版本 | 用�?| 安装方式 |
|------|------|------|----------|
| jq | 1.6+ | hook 脚本 JSON 解析（推荐） | `D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\install_jq_rg.ps1` |
| Claude Code | latest | 外部代理委派 | `npm install -g @anthropic-ai/claude-code` |
| Codex | latest | 外部代理委派 | `npm install -g @openai/codex` |

### 支持平台

| 平台 | 状�?| 备注 |
|------|------|------|
| macOS | �?完全支持 | 原生 bash |
| Linux | �?完全支持 | 原生 bash |
| Windows | ⚠️ 支持 | 需安装 Git Bash |

### 环境检查脚�?```bash
# 检查必需依赖
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\check-environment.py

# 输出示例:
# �?Python 3.11.5
# �?Git 2.42.0
# �?bash 5.2.15
# ⚠️ jq 未安装（hook 脚本将使�?bash fallback�?```

## Git 集成与回滚（v10.2 新增�?迭代改进可能产生破坏性修改，loop-controller 集成 Git 自动回滚�?### 自动提交

```bash
# 初始化时启用自动提交
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py init \
  --name "性能优化" \
  --mode max --max 10 \
  --auto-commit

# 每次迭代前自动创建临时提�?# git commit -m "chore: pre-iteration snapshot (loop: 性能优化, iter: 3)"
```

### 回滚

```bash
# 回滚到指定迭�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py rollback --name "性能优化" --to 2

# 回滚到上一次迭�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py rollback --name "性能优化" --prev

# 回滚到循环开始前
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\loop-controller.py rollback --name "性能优化" --initial
```

### 回滚机制

1. 每次迭代前创�?Git tag: `loop/{name}/iter/{n}`
2. 回滚�?`git checkout` 到对�?tag
3. 保留所有迭代历史，可随时恢�?## 本能学习系统（v10.4 新增�?从编码实践中学习模式/规则，自动积累编码本能。脚本：`D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\instinct-manager.py`。支持记录、查询、衰减、晋升。按项目隔离存储�?## 工作流编排（v10.4 新增�?支持完整的开发生命周期编排：分类 �?规划 �?执行 �?审查 �?优化�?### 模式 5：工作流编排（v11.0 增强�?触发：用户要求完整开发一个功�?/ "develop" / "实现这个功能"

流程�?1. **任务分类** �?frontend / backend / fullstack
2. **规划阶段** �?上下文检�?+ 实现计划（只读）
3. **用户确认计划**
4. **🌳 创建隔离工作�?*（v11.0 新增）：
   ```bash
   python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\worktree-manager.py create --name "{task-name}" --base master
   ```
   - �?`.worktrees/{task-name}/` 创建隔离工作�?   - 自动创建同名分支
   - 后续步骤�?worktree 中执行，主分支保持干净
   - ⚠️ 如果任务简单（< 3 文件修改），可跳�?worktree
5. **执行阶段** �?�?worktree 中按计划修改代码
6. **🔍 审查阶段**（v11.2 增强）→ 自动调用 `code-review` skill
   - 根据任务复杂度选择审查深度�?     - medium �?**快速审�?*�?代理�?     - large �?**标准审查**�?代理并行�?     - 关键模块/安全敏感 �?**深度审查**�?代理并行�?   - 审查发现 �?修复后进入优化阶�?   - 调用方式：`read D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\code-review\SKILL.md` �?按其流程执行
7. **优化阶段** �?根据审查结果修复
8. **交付确认** �?用户选择�?   - **合并**：`git merge {branch}` �?`worktree-manager.py cleanup --merged`
   - **保留**：保�?worktree 继续开�?   - **丢弃**：`git worktree remove .worktrees/{name}` + `git branch -D {branch}`

**Worktree 管理命令**�?```bash
# 创建隔离工作�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\worktree-manager.py create --name "feature-x"

# 列出所�?worktree
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\worktree-manager.py list

# 查看 worktree 状�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\worktree-manager.py status --name "feature-x"

# 清理已合并的 worktree
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\worktree-manager.py cleanup --merged

# 切换�?worktree 目录
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\worktree-manager.py switch --name "feature-x"
```

**执行完后输出上下文摘�?*（v10.9 新增）：
```
[Workflow] 开发完�?�?📚 上下�? 145k/203k (71%) | 🧮 本次: +25.3k tokens
```
调用 session_status 工具提取关键信息，输出一行简洁摘要�?### 模式 6：Plan Mode（结构化计划）（v10.9 新增�?> 借鉴 Copilot CLI �?Plan Mode：先做结构化计划（输出带 checkbox �?plan.md），等用户确认后再执行，执行时逐条勾选�?**触发**�?- 用户�?先做个计�? / "plan" / "规划一�? / "做个方案"
- 在模�?-5中按 Shift+Tab（或手动）切换到计划模式
- 复杂任务自动建议�?这个任务比较复杂，建议先做计划？"

**流程**�?```
1. 分析需求（只读，不修改代码�?   ├─ 读取相关文件
   ├─ 理解现有架构
   └─ 识别依赖关系

2. 生成 plan.md（带 checkbox�?   ├─ 任务分解为可执行步骤
   ├─ 每个步骤�?checkbox: - [ ]
   ├─ 标注依赖关系（步骤间的先后顺序）
   ├─ 估算每步耗时
   └─ 保存�?plans/plan-YYYYMMDD-HHMMSS.md

3. 等待用户确认
   ├─ 用户�?执行" / "开�? / "go" �?进入执行阶段
   ├─ 用户修改计划 �?更新 plan.md
   └─ 用户�?取消" �?终止

4. 逐条执行 + 勾�?   ├─ 完成一�?�?- [x]
   ├─ 遇到问题 �?记录原因，继续下一步或暂停
   └─ 全部完成 �?输出总结
```

**plan.md 格式规范**�?```markdown
# Implementation Plan: {功能名称}

## Overview
{一句话描述目标}

## Context
- 相关文件: file1.py, file2.ts, ...
- 依赖: �?/ moduleA, moduleB
- 预计耗时: ~30 分钟

## Tasks

### Phase 1: 基础设施
- [ ] 创建数据模型 `models/user.py` (~5min)
- [ ] 编写数据库迁移脚�?(~3min)

### Phase 2: 核心逻辑
- [ ] 实现 API 端点 `api/auth.py` (~10min)
  - 依赖: Phase 1 完成
- [ ] 编写单元测试 `tests/test_auth.py` (~8min)

### Phase 3: 集成
- [ ] 前端对接 `pages/Login.tsx` (~10min)
  - 依赖: Phase 2 API 完成
- [ ] 端到端测�?(~5min)

## Risks
- 风险1: 第三�?API 可能不稳�?�?降级方案: mock
- 风险2: ...

## Notes
- 备注1: ...
```

**执行阶段输出**�?```
[Plan] 执行�?.. (3/6)
�?创建数据模型 models/user.py
�?编写数据库迁移脚�?�?实现 API 端点 api/auth.py
�?编写单元测试 tests/test_auth.py  �?当前
�?前端对接 pages/Login.tsx
�?端到端测�?进度: 50% | 已用�? 15min | 预计剩余: 15min
```

**与模�?的区�?*�?- 模式5：完整的"开发→审查→优�?流水线，适用�?实现整个功能"
- 模式6：纯粹的"计划→确认→执行"，适用�?先理清思路再动�?，可独立使用

**执行完后输出上下文摘�?*（v10.9 新增）：
```
[Plan] 执行完成 (6/6) �?📚 上下�? 125k/203k (62%) | 🧮 本次: +8.2k tokens
```
调用 session_status 工具提取关键信息，输出一行简洁摘要�?**文件结构**�?```
plans/
  plan-20260703-103000.md    # 计划文件
  plan-20260703-143000.md
```

#### PDD 规格驱动模式（v11.4 新增，方案B�?> 借鉴 ralph-orchestrator �?Plan-Driven Development：大型功能使�?.specs/ 目录结构，将需�?设计/实现计划分离为独立文档�?**触发条件**�?- 复杂�?= large �?critical
- 用户�?做个详细设计" / "�?spec" / "PDD"
- 涉及多模块、多文件、多阶段的复杂功�?**流程**�?```
1. 创建 Spec 目录
   python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\spec-init.py "功能名称"
   # 生成 .specs/feature-name/ 目录

2. 填写需�?�?requirements.md
   ├─ 用户故事
   ├─ 验收标准（Given/When/Then�?   ├─ 边界条件
   └─ 非功能需�?
3. 技术设�?�?design.md
   ├─ 架构概览
   ├─ 数据模型
   ├─ API 设计
   ├─ 安全考虑
   └─ 备选方案对�?
4. 实现计划 �?implementation-plan.md
   ├─ 分阶段任务清单（每步 �?30分钟�?   ├─ DAG 依赖�?   ├─ 每步的验证标�?   └─ 风险评估

5. 用户确认 �?逐阶段执�?+ Backpressure 门控
```

**Spec 目录结构**�?```
.specs/
  feature-name/
    README.md               # 索引（状�?链接�?    requirements.md         # What �?需�?    design.md               # How �?设计
    implementation-plan.md  # Steps �?实现步骤
    context.md              # Why �?背景约束（可选）
```

**脚手架命�?*�?```bash
# 创建 spec（默认模板）
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\spec-init.py "Add JWT authentication"

# 创建 spec（API 模板�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\spec-init.py "User management API" --template api

# 创建 spec（简单模式，�?context.md�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\spec-init.py "Fix login bug" --simple

# 列出所�?specs
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\spec-init.py --list
```

**与简�?Plan Mode 的选择**�?| 场景 | 选择 | 原因 |
|------|------|------|
| trivial/small 任务 | 简�?plan.md | 轻量，一步到�?|
| medium 任务 | 简�?plan.md | 够用 |
| large 任务 | PDD .specs/ | 需要设�?计划分离，便于追�?|
| critical 任务 | PDD .specs/ | 完整文档，团队可审查 |

### 模式 7：Explore 侦察（v10.9 新增�?> 借鉴 Copilot CLI �?Explore 代理：在独立上下文中快速侦察代码库，返回结论摘要，不污染主会话�?**触发**�?- 用户�?这个文件有多�? / "有多少个测试文件" / "这个函数被谁调用"
- 编码前需要了解项目结�?- 不确定某个模块的依赖关系
- 快速验证假设（"有没有循环依赖？"�?**�?code-reviewer 的区�?*�?| 维度 | code-reviewer | Explore |
|------|---------------|---------|
| 深度 | 深度审查，输出详细报�?| 快速侦察，输出结论摘要 |
| 上下�?| 完整上下�?| 独立上下文，不污染主会话 |
| 输出 | Markdown 报告 | 结构�?JSON |
| 耗时 | 2-5 分钟 | 30-60 �?|
| 类比 | 体检报告 | 体温计读�?|

**执行方式**�?```
sessions_spawn(
  task: "你是 explore 侦察代理。快速回答以下问题，返回结论摘要�?         问题：{user_question}
         
         输出格式（严�?JSON）：
         {\"question\": \"原始问题\", \"answer\": \"结论摘要\", \"details\": {...}, \"confidence\": \"high|medium|low\"}
         
         规则�?         - 只读，不修改任何文件
         - 返回具体数字、路径、名�?         - 不输出完整文件内�?         - 不做深度分析",
  model: "sonnet",
  mode: "run",
  runTimeoutSeconds: 60,
  tools: ["Read", "Grep", "Glob", "exec"]
)
```

**典型任务**�?- 文件大小/行数统计
- 目录结构概览
- 函数/类的调用关系
- 依赖关系查询
- 测试文件映射
- 快速验证假�?**输出示例**�?```json
{
  "question": "src/utils.py 有多少行�?,
  "answer": "src/utils.py �?342 �?,
  "details": {"file": "src/utils.py", "lines": 342},
  "confidence": "high"
}
```

**Token 预算控制**�?- 只传入问题，不传入整个项�?- 输出限制 500 tokens
- 超时 60 �?**执行完后输出上下文摘�?*（v10.9 新增）：
```
[Explore] 侦察完成
📚 上下�? 122k/203k (60%) | 🧮 本次: +2.1k tokens
```
调用 session_status 工具提取关键信息，输出一行简洁摘要�?### Mode X: Debug（v12.2 新增，P0，Feedback Loop First�?> 来源：DeepSeek 评审 P0 方案 �?"没有 red-capable 命令就不进入 Phase 2"
> 核心原则�?*调试的本质是构建反馈循环，而非猜测修复�?*

#### 铁律

```
NO RED-CAPABLE COMMAND = NO PHASE 2
```

如果你无法输出一�?能变红的命令"（即能证�?bug 存在的失败测�?脚本），你不允许进入修复阶段�?#### 6 阶段流程

```
Phase 1: Build Feedback Loop
    ├─ 目标：构建一个能复现 bug 的自动化命令
    ├─ 输出：一个可执行的命令（test/script/curl/harness�?    ├─ 检查点：⚠�?必须输出"能变红的命令"才能进入 Phase 2
    └─ 强制门控�?        ├─ 输出命令 �?运行 �?确认失败（red）→ 进入 Phase 2 �?        ├─ 无法输出命令 �?继续尝试构建 �?最�?3 种方�?        └─ 3 种方式均失败 �?报告用户，请求帮�?
Phase 2: Reproduce + Minimise
    ├─ 目标：确�?bug 可复现，并最小化复现条件
    ├─ 运行 Phase 1 的命�?�?确认 red
    ├─ 逐步移除无关变量（输入数�?配置/环境�?    └─ 输出：最小复现用�?+ 运行命令

Phase 3: Hypothesise
    ├─ 目标：基于最小复现，提出 1-3 个根因假�?    ├─ 每个假设必须可证伪（能设计实验验证）
    ├─ 按可能性排�?    └─ 输出：假设列�?+ 验证方法

Phase 4: Instrument
    ├─ 目标：在关键路径添加调试日志/断点
    ├─ 使用 Tagged Debug Logs（见下方规范�?    ├─ 日志必须包含假设验证所需信息
    └─ 输出：插桩代�?+ 预期输出

Phase 5: Fix + Regression
    ├─ 目标：修�?bug + 添加回归测试
    ├─ 基于 Phase 3 的假设验证结果修�?    ├─ 运行 Phase 1 的命�?�?确认 green
    ├─ 添加回归测试（防止同�?bug 再次出现�?    └─ 输出：修复代�?+ 回归测试 + 验证证据

Phase 6: Cleanup
    ├─ 目标：清理调试代码，恢复代码整洁
    ├─ 删除所�?[DEBUG-*] 日志
    ├─ 删除临时 harness/fixture
    ├─ 运行完整测试套件确认无回�?    └─ 输出：清理后的代�?+ 最终验证证�?```

#### Phase 1 强制检查点

```
╔════════════════════════════════════════════════════════════╗
�?Phase 1 检查点 �?必须满足以下条件才能进入 Phase 2        �?╠════════════════════════════════════════════════════════════╣
�?                                                          �?�?1. 已输出一个具体命令（不是"应该运行XXX"�?              �?�?2. 该命令能独立运行（无需人工干预�?                      �?�?3. 该命令当前会失败（red�?                               �?�?4. 失败原因�?bug 本身（不是环�?配置问题�?              �?�?                                                          �?�?输出格式�?                                               �?�?```                                                       �?�?[Phase 1 Checkpoint]                                      �?�?Command: <具体命令>                                       �?�?Expected failure: <失败描述>                              �?�?Actual output: <实际输出>                                 �?�?Status: RED �?�?进入 Phase 2                            �?�?```                                                       �?�?                                                          �?�?如果无法输出命令 �?不允许进�?Phase 2                     �?╚════════════════════════════════════════════════════════════╝
```

#### 10 种反馈循环构建方式（�?OpenClaw 环境可用性排序）

| 优先�?| 方式 | 适用场景 | 示例 |
|--------|------|----------|------|
| 1 | **Failing Test** | 有测试框架的项目 | `pytest tests/test_bug.py -v` / `npm test -- --grep "bug"` |
| 2 | **Curl/HTTP Script** | API/服务�?bug | `curl -X POST localhost:3000/api/bug-endpoint -d '{}'` |
| 3 | **CLI Invocation + Fixture** | CLI 工具 bug | `python cli.py process --input fixture.json` |
| 4 | **Throwaway Harness** | 无测试框架的函数/模块 | 临时 Python/JS 脚本调用目标函数 |
| 5 | **HITL Bash Script** | 需要人工验证的 UI/视觉 bug | `bash verify.sh`（最后手段，需人工确认�?|
| 6 | **Log Grep Pattern** | 日志中可追踪的错�?| `grep "ERROR_PATTERN" app.log \| wc -l` |
| 7 | **Exit Code Check** | 进程崩溃/异常退�?| `python script.py; echo $?` |
| 8 | **Diff Comparison** | 输出不一�?bug | `diff expected.txt actual.txt` |
| 9 | **Timeout Detection** | 性能/死锁 bug | `timeout 5s python script.py; echo $?` |
| 10 | **Memory/Resource Check** | 内存泄漏/资源耗尽 | `python -c "import resource; ..."` |

**选择原则**�?- 优先使用编号小的方式（更可靠、更易自动化�?- 方式 1-4 �?agent 可独立运行的（满�?Tight Loop 条件�?- 方式 5 需要人工介入，只在无其他选择时使�?#### Tagged Debug Logs 规范

所有调试日志使用唯一前缀，便于清理和追踪�?```
格式：[DEBUG-<4位随机hex>] <消息>

示例�?[DEBUG-a4f2] Entering function process_order() with input: {id: 123}
[DEBUG-a4f2] Database query returned: 0 rows
[DEBUG-a4f2] Hypothesis check: expected 1 row, got 0 �?CONFIRMED

规则�?1. 每次调试会话使用同一�?tag（如 a4f2�?2. tag �?Phase 4（Instrument）开始时生成
3. 所有调试日志必须带 tag
4. Phase 6（Cleanup）时删除所有带 tag 的行
```

**清理命令**�?```bash
# 查找所有调试日�?grep -r "\[DEBUG-a4f2\]" src/

# 删除所有调试日志（sed�?sed -i '/\[DEBUG-a4f2\]/d' src/**/*.py
```

#### Tight Loop 四条�?反馈循环必须同时满足以下 4 个条件，否则需要调整：

| 条件 | 说明 | 检查方�?|
|------|------|----------|
| **Red-capable** | 当前能失败（证明 bug 存在�?| 运行命令，确认非零退出码或失败输�?|
| **确定�?* | 每次运行结果一致（�?flaky�?| 连续运行 3 次，结果相同 |
| **快速（秒级�?* | 运行时间 < 10 �?| `time <command>` |
| **Agent 可独立运�?* | 无需人工干预 | agent 能自动运行并解析输出 |

**不满足时的处�?*�?| 不满足条�?| 处理方式 |
|-----------|----------|
| �?red-capable | 检查输入数�?环境配置，确保触�?bug 路径 |
| 非确定�?| 固定随机种子/mock 外部依赖/隔离环境 |
| 非快�?| 减少测试数据规模/mock 慢依�?只运行相关测�?|
| 非独立运�?| 改用其他方式（从 HITL �?Throwaway Harness �?Test�?|

#### 反模式警�?| 你的想法 | 现实 |
|---------|------|
| "我直接看代码就知�?bug 在哪" | 知道 �?证明。先构建反馈循环。|
| "这个 bug 太明显了，不需要测�? | 明显�?bug 也可能修错地方。用命令验证。|
| "先修了再�? | 修了没有验证 = 猜测。Phase 1 先。|
| "构建测试太麻�? | 不构建测�?= 没有反馈循环 = 盲修。|
| "用眼睛看日志就够�? | 眼睛不可靠。用 grep/命令自动化。|

#### 与其他模式的关系

- **Mode 1（快速编码）**：Mode X �?Mode 1 步骤 3（验证失败）时自动触�?- **Mode 3（迭代改进）**：Mode X �?Phase 5 修复后可进入 Mode 3 优化
- **systematic-debugging skill**：Mode X 是框架级入口，systematic-debugging 是详细流�?- **verification-before-completion**：Mode X Phase 5 的修复必须通过 verification 门控

---

### 模式 9：三角色切换（v12.1 新增，P2�?> 来源：Superpowers 的多角色审查设计
> 核心思想�?*无需子代�?*，在同一会话中切�?Implementer/Reviewer/Fixer 三个角色，实现自我审查和修复�?#### 为什么需要？
- 子代理有额外 token 开销和延�?- 简单任务的代码审查不需要独立上下文
- 角色切换强制 AI 从不同视角审视代码，减少盲点

#### 三个角色

| 角色 | 职责 | 视角 | 输出 |
|------|------|------|------|
| **Implementer** | 编写代码 | "如何实现需�? | 代码 + 实现说明 |
| **Reviewer** | 审查代码 | "这段代码有什么问�? | 问题列表 + 严重�?|
| **Fixer** | 修复问题 | "如何精准修复" | 修复代码 + 验证结果 |

#### 流程

```
角色 1: Implementer
    ├─ 按需求编写代�?    ├─ 完成�?�?明确标记 "[Implementer] 实现完成"
    └─ 输出代码 + 实现说明
         �?角色 2: Reviewer（切换！�?    ├─ 以审查者视角阅读代�?    ├─ 检查维度：
    �?  ├─ 正确性：是否实现需求？
    �?  ├─ 安全性：有无安全漏洞�?    �?  ├─ 简洁性：有无过度工程�?    �?  ├─ 边界条件：是否处理边界？
    �?  └─ 风格：是否符合项目规范？
    ├─ 输出问题列表（按严重度排序）
    └─ 明确标记 "[Reviewer] 审查完成"
         �?    有问题？
    ├─ �?�?完成 �?    └─ �?�?进入 Fixer 角色
         �?角色 3: Fixer（切换！�?    ├─ 逐个修复 Reviewer 发现的问�?    ├─ 每个修复后验�?    └─ 明确标记 "[Fixer] 修复完成"
         �?    回到 Reviewer 角色（再次切换！�?    ├─ 验证修复是否有效
    └─ 无新问题 �?完成 �?```

#### 角色切换标记

每次角色切换时，输出明确标记�?```
---
🔄 角色切换: Implementer �?Reviewer
---

[Reviewer 视角]
审查以下代码...
```

```
---
🔄 角色切换: Reviewer �?Fixer
---

[Fixer 视角]
修复问题 1: ...
```

#### 触发条件

- 用户�?自我审查" / "三角�? / "self-review"
- 任务复杂�?= medium（不需�?spawn 子代理，但需要审查视角）
- 模式 1 步骤 6 的轻量替代（trivial/small 任务用🦆自审，medium 用三角色，large 用子代理审查�?#### 与子代理审查的区�?| 维度 | 三角色模�?| 子代理审�?|
|------|-----------|-----------|
| 上下�?| 同一会话 | 独立上下�?|
| Token 开销 | 低（无额外上下文�?| 高（每个子代理独立上下文�?|
| 审查深度 | 中等 | 深度 |
| 适用复杂�?| medium | large/critical |
| 速度 | �?| �?|

#### 强制规则

- 角色切换�?*必须**输出明确标记�?🔄 角色切换"�?- Reviewer 角色**必须**输出问题列表（即使没有问题也要说"无问�?�?- Fixer 角色**必须**验证每个修复
- 禁止跳过 Reviewer 角色直接进入 Fixer

### 任务分类路由

| 任务类型 | 特征关键�?| 主责代理 | 协助代理 |
|----------|------------|----------|----------|
| frontend | component, UI, 页面, 组件, 样式 | typescript-reviewer | code-reviewer |
| backend | API, database, 接口, 算法 | python-reviewer | security-auditor |
| fullstack | 默认 | code-reviewer | ts-reviewer + py-reviewer |

### 使用方法

```bash
# 分类任务
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\workflow-orchestrator.py classify \
  --description "实现用户登录页面" \
  --files "src/pages/Login.tsx"

# 生成实现计划（只读）
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\workflow-orchestrator.py plan \
  --description "实现用户登录功能" \
  --files "src/pages/Login.tsx,src/api/auth.py"

# 执行计划
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\workflow-orchestrator.py execute --plan "plans/plan-xxx.json"

# 审查代码
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\workflow-orchestrator.py review \
  --files "src/pages/Login.tsx" \
  --auto-select

# 完整流水�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\workflow-orchestrator.py pipeline \
  --description "实现用户登录功能" \
  --files "src/"
```

### 专属代理

| 代理 | 审查重点 |
|------|----------|
| frontend-reviewer | UI/UX、组件设计、响应式布局、可访问性、动�?|
| backend-reviewer | API 设计、数据库操作、算法、业务逻辑、安�?|

### 规划与执行分�?- **规划阶段**：只读，不修改代码，生成实现计划
- **执行阶段**：按计划修改代码
- **好处**：避�?边想边做"的质量问题，用户可先审核计划

## DAG 任务调度（v10.5 新增�?将大需求分解为有依赖关系的任务 DAG（有向无环图），按拓扑排序和复杂度分层执行�?### 核心概念

| 概念 | 说明 |
|------|------|
| WorkUnit | 一个独立的工作单元（任务） |
| Dependency | 任务间的依赖关系（前置任务） |
| Complexity | 复杂度等级（trivial/small/medium/large�?|
| Stage | 执行阶段（plan/execute/review/optimize�?|

### 复杂度分层与质量流水�?不同复杂度走不同深度的质量流水线�?| 复杂�?| 权重 | 质量流水�?| 审查深度 | 预计耗时 |
|--------|------|------------|----------|----------|
| trivial | 1 | execute | 无（路径A自审已覆盖） | 5 分钟 |
| small | 2 | execute �?review | 路径A自审（提示词级） | 15 分钟 |
| medium | 4 | plan �?execute �?🦆 �?🔍code-review(快�? | 路径B自审 + code-review快速审查（1代理�?| 30 分钟 |
| large | 8 | plan �?execute �?🦆 �?🔍code-review(标准) �?optimize | 路径B自审 + code-review标准审查�?代理�?| 60 分钟 |

**设计原则**�?- trivial/small 任务跳过规划阶段，直接执�?- small 任务依赖路径A"🦆自审"（模�?步骤4），不额外spawn子代�?- **medium+ 任务自动触发路径B的rubber-duck**：execute完成后，daily-agent收尾检查自动spawn轻量审查子代�?- large 任务需要完整的规划-执行-审查-优化流水�?- 审查深度随复杂度递增，避免过度审查简单任�?**🦆 Rubber Duck 自动触发规则（v10.9 新增�?*�?```
execute 阶段完成
  �?daily-agent 收尾检�?  ├─ 任务类型 = 编码类？ �?跳过
  ├─ 复杂�?�?medium�?�?跳过（路径A自审已覆盖）
  ├─ 用户已显式要求审查？ �?跳过（避免重复）
  └─ 满足全部条件 �?自动 spawn rubber-duck 子代�?       ├─ verdict: "pass" �?静默通过，继�?review 阶段
       └─ verdict: "fail" �?issues 注入主会话，修复后进�?review 阶段
```

**🔍 Code-Review 自动触发规则（v11.2 新增�?*�?```
代码编写完成 + 验证通过（L1+L2�?  �?自动审查决策
  ├─ 任务复杂�?= trivial / small �?跳过（🦆自审已覆盖�?  ├─ 用户�?不需要审�? / --skip-review �?跳过
  ├─ 用户已显式调�?code-review �?跳过（避免重复）
  └─ 满足条件 �?自动调用 code-review skill
       ├─ medium 任务 �?快速审查（1代理，~30秒）
       ├─ large 任务 �?标准审查�?代理�?-2分钟�?       └─ 关键模块/安全敏感 �?深度审查�?代理�?-5分钟�?            ├─ 发现 high/critical �?修复后再输出
            └─ 无高置信度问�?�?直接输出
```

### 使用方法

```bash
# 1. 创建 DAG
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py create \
  --name "user-auth" \
  --description "实现用户认证功能"

# 2. 添加任务（指定复杂度�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py add \
  --dag "user-auth" \
  --id "db-model" \
  --description "创建用户表模�? \
  --complexity "small"

python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py add \
  --dag "user-auth" \
  --id "api-endpoints" \
  --description "实现登录/注册 API" \
  --complexity "medium"

python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py add \
  --dag "user-auth" \
  --id "frontend-login" \
  --description "实现登录页面" \
  --complexity "large"

# 3. 添加依赖关系
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py depend \
  --dag "user-auth" \
  --from "api-endpoints" \
  --to "db-model"

python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py depend \
  --dag "user-auth" \
  --from "frontend-login" \
  --to "api-endpoints"

# 4. 生成执行计划（拓扑排序）
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py schedule --dag "user-auth"

# 5. 获取下一个可执行任务
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py next --dag "user-auth"

# 6. 更新任务状�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py update \
  --dag "user-auth" \
  --id "db-model" \
  --status "completed"

# 7. 查看 DAG 状�?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py status --dag "user-auth"
```

### 执行流程

```
1. create DAG �?定义需�?2. add tasks �?分解为工作单元（指定复杂度）
3. depend �?建立依赖关系
4. schedule �?拓扑排序，生成执行顺�?5. next �?获取下一个可执行任务
   └─ 根据复杂度自动匹配质量流水线
   └─ trivial: 直接执行
   └─ small: 执行 + 轻量审查
   └─ medium: 规划 + 执行 + 标准审查
   └─ large: 规划 + 执行 + 深度审查 + 优化
6. update �?更新任务状�?7. 循环 5-6 直到所有任务完�?```

### 并行执行

无依赖关系的任务可以并行执行�?```bash
# 查看哪些任务可以并行
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\coding-framework\scripts\dag-scheduler.py schedule --dag "feature-x"
# 输出�?can_parallel: true 的任务可并行
```

### 目录结构

```
dags/
  {dag-name}.json    # DAG 定义文件
```

---

## Step 7: Progress Ledger（v12.0 新增�?> 来源：Superpowers subagent-driven-development �?durable progress 设计
> DS评审修正：补充完整恢复流�?+ 冲突处理 + 自动清理

### 为什么需要？
长任务执行中，compaction 会丢失上下文。如�?AI "忘记"哪些任务已完成，会重�?dispatch 子代理，浪费 token 和时间�?### 机制

1. **创建账本文件**：`.superpowers/progress.md`（git-ignored�?2. **任务完成时追�?*：`Task N: complete (commits <base7>..<head7>, review clean)`
3. **恢复时读�?*：compaction 后，先读账本 + `git log`，再决定从哪个任务继�?4. **不重�?dispatch**：账本标�?complete 的任务，不再重新执行

### 账本格式

```markdown
# Progress Ledger
Created: 2026-07-14 17:30

Task 1: complete (commits a1b2c3d..e4f5g6h, review clean)
Task 2: complete (commits e4f5g6h..i7j8k9l, review clean)
Task 3: in_progress (dispatched at 17:45)
```

### 完整恢复流程（DS修正版）

```
任务开始时�?└─ 读取 .superpowers/progress.md
    ├─ 存在 �?读取 git log --oneline -20
    �?       └─ 比对账本中的 commit hash
    �?           ├─ 匹配 �?从最后一�?complete 任务的下一个继�?    �?           └─ 不匹�?�?标记【警告：账本可能过期】，人工确认
    └─ 不存�?�?�?Task 1 开�?
任务完成时：
└─ 追加写入 .superpowers/progress.md
    ├─ 获取当前 commit hash: git rev-parse --short HEAD
    ├─ 格式: Task N: complete (commits <start>..<end>, review clean)
    └─ flush 写入（确保持久化�?
检�?compaction 信号�?├─ 用户�?继续" / "刚才我们做到哪了"
├─ AI 发现自己在重新询问已讨论过的问题
└─ 主动检�?�?"检测到对话压缩，正在读取进度账�?.."
```

### 账本冲突处理

| 场景 | 处理 |
|------|------|
| 账本有记录，commit 匹配 | 正常继续 |
| 账本有记录，commit 不匹�?| **暂停**：展示差异，请求用户确认 |
| 账本有记录，git log 找不到该 commit | **暂停**：账本可能损坏或来自其他分支 |
| 账本为空，但 git 有未记录提交 | **警告**：可能存在未记录的工�?|

### 账本生命周期

- 任务开始时创建：`.superpowers/progress.md`
- 任务完成后保�?24 小时
- 超过 24 小时的账本可自动归档/删除
- **不进�?git 版本控制**

---

## Step 8: Verification Before Completion

铁律：没有新鲜验证证据，不能声称完成。详�?`verification-before-completion` skill�?---

## 版本历史

当前版本：v13.0.0�?026-07-24）。完整历史见 git log�?
---

## 子模式路由系统（v13.0.0 新增�?
> 通过触发词自动路由到对应开发模式。无匹配时使用默认框架流程�?
### 路由规则

| 触发�?| 子模�?| 条件指令 |
|--------|--------|---------|
| "TDD"/"红绿重构"/"测试先行"/"测试驱动" | mode: tdd | 仅当用户提到TDD/测试驱动时加�?|
| "增量实现"/"薄切�?/"垂直切片"/"incremental" | mode: incremental | 仅当用户提到增量开�?切片实现时加�?|
| "规格驱动"/"PRD"/"需求文�?/"spec-driven" | mode: spec-driven | 仅当用户提到规格驱动/PRD/需求文档时加载 |
| "CoreCoder"/"Claude Code核心"/"corecoder" | mode: corecoder | 仅当用户明确要求CoreCoder模式时加�?|
| "执行脚手�?/"规划→TDD→审�?/"implement" | mode: implement | 仅当用户要求完整实现串联时加�?|
| 无匹�?| 默认 | 使用标准框架流程 |

### 路由优先�?
1. 用户明确指定模式 �?直接使用对应子模�?2. 触发词匹�?�?自动路由
3. 多触发词匹配 �?优先选择最具体的（�?TDD增量实现"�?mode: tdd + incremental 叠加�?4. 无匹�?�?默认框架流程（Step 0-8�?
---

<!-- sub-mode: tdd -->
## 子模式：TDD红绿重构（合并自test-driven-development v1.0.0�?
> 仅当用户提到TDD/测试驱动/红绿重构/测试先行时加载本节�?
### 核心理念
先写失败测试，再写让测试通过的最少代码，然后重构。测试是证明—�?看起来对"不算完成�?
### TDD循环
```
  RED                GREEN              REFACTOR
写失败测�?  ──�? 写最少代码通过  ──�? 清理实现  ──�?(重复)
```

### 步骤
1. **RED** �?写一个失败的测试（基于验收标准）。它必须失败。立即通过的测试什么也证明不了�?2. **GREEN** �?写最少代码让测试通过。不要过度工程�?3. **REFACTOR** �?在测试保护下重构。提取共享逻辑、改进命名、消除重复。每次重构后运行测试�?
### 各步骤完成条�?- **RED**：测试已编写并运行，确认失败（exit code �?0），失败原因是目标功能尚未实�?- **GREEN**：最少实现代码已编写，测试全部通过（exit code = 0），无过度工�?- **REFACTOR**：实现代码已清理，测试仍全部通过，代码行数未增加

### Prove-It模式（Bug修复�?收到Bug报告时，**不要从尝试修复开�?*。先写一个复现它的测试：
```
Bug报告到达 �?写一个展示Bug的测�?�?测试失败（确认Bug存在）→ 实现修复 �?测试通过（证明修复有效）�?运行完整测试套件（无回归�?```

### 测试金字�?- 单元测试(~80%)：纯逻辑，隔离，毫秒�?- 集成测试(~15%)：组件交互，API边界
- E2E测试(~5%)：完整用户流程，真实浏览�?
### 写好测试的原�?- **测试状态，而非交互** �?断言操作的结果，而非内部调用
- **DAMP优于DRY** �?测试中描述性优于抽象�?- **优先真实实现而非Mock** �?真实实现 > fake > stub > mock
- **Arrange-Act-Assert模式** �?每个测试清晰三段�?
### 测试反模�?| 反模�?| 修复 |
|--------|------|
| 测试实现细节 | 测试输入和输�?|
| 不稳定测�?| 使用确定性断言，隔离状�?|
| 测试框架代码 | 只测�?你的*代码 |
| Mock一�?| 仅在边界处mock |

### 约束
- 测试先行：代码之前必须有失败测试
- 最少代码：只写让测试通过的代�?- Prove-It：Bug修复从复现测试开�?- 每个概念一个断言
- 描述性命名测�?
<!-- /sub-mode: tdd -->

---

<!-- sub-mode: incremental -->
## 子模式：薄垂直切片增量实现（合并自incremental-implementation v1.0.0�?
> 仅当用户提到增量开�?切片实现/垂直切片/薄切片时加载本节�?
### 核心理念
Build in thin vertical slices �?实现一块、测试、验证、再扩展。每个增量都让系统处于可工作状态�?
### 增量循环
```
Implement �?Test �?Verify �?Commit �?Next slice
```

对每个切片：
1. **实现** 最小完整功能块
2. **测试** �?运行测试套件
3. **验证** �?确认切片按预期工�?4. **提交** �?用描述性消息保存进�?5. **进入下一切片** �?前进，不重启

### 切片策略

**策略1: 垂直切片（首选）** �?构建完整的端到端路径�?```
切片1: 创建任务（DB + API + 基础UI）→ 测试通过
切片2: 列出任务（查�?+ API + UI）→ 测试通过
切片3: 编辑任务（更�?+ API + UI）→ 测试通过
切片4: 删除任务（删�?+ API + UI + 确认）→ 完成CRUD
```

**策略2: 契约优先切片** �?前后端并行开发时先定义API契约

**策略3: 风险优先切片** �?先处理最高风险或最不确定的部分

### 5条实现规�?- **Rule 0: 简单优�?* �?三行相似代码好过早熟抽象
- **Rule 0.5: 范围纪律** �?只碰任务需要的东西
- **Rule 1: 一次一件事** �?不混合关注点
- **Rule 2: 保持可编�?* �?每个增量后项目必须能构建
- **Rule 3: Feature Flags** �?保护未完成功�?- **Rule 4: 安全默认** �?新代码默认安全保守行�?- **Rule 5: 回滚友好** �?每个增量可独立回�?
### 增量检查清�?- [ ] 变更做一件事且完整做�?- [ ] 所有现有测试通过
- [ ] 构建成功
- [ ] 类型检查通过
- [ ] Lint通过
- [ ] 变更已提交，消息描述�?
### 红旗
- 写超�?00行代码没运行测试
- 单个增量中多个不相关变更
- 切片间构建或测试破损
- 在第三个用例要求前构建抽�?
<!-- /sub-mode: incremental -->

---

<!-- sub-mode: spec-driven -->
## 子模式：规格驱动开发（合并自spec-driven-development v1.0.0�?
> 仅当用户提到规格驱动/PRD/需求文�?功能规格时加载本节�?
### 核心理念
在写任何代码之前先写结构化规格文档。规格是你与人类工程师之间的共享真相来源。没有规格的代码就是猜测�?
### 门控工作�?```
规格说明 �?计划 �?任务 �?实现
  �?         �?     �?     �?人类审查   人类审查  人类审查  人类审查
```

### 阶段1: 规格说明
从高层愿景开始。向人类提出澄清问题，直到需求具体化�?
**立即浮出假设** �?在写任何规格内容之前，列出你的假设�?
**编写覆盖六个核心领域的规格文�?*�?1. **目标** �?构建什么？为什么？用户是谁�?2. **命令** �?完整的可执行命令和标�?3. **项目结构** �?源代码、测试、文档位�?4. **代码风格** �?真实代码片段展示风格
5. **测试策略** �?框架、位置、覆盖率期望
6. **边界** �?三层：总是�?先问/绝不�?
### 阶段2: 计划
识别主要组件及依赖、实现顺序、风险、并行可能性、验证检查点�?
### 阶段3: 任务
分解为离散可实现任务，每个任务有验收标准和验证步骤�?
### 阶段4: 实现
逐个执行任务，遵循incremental-implementation和test-driven-development�?
### 规格模板
```markdown
# 规格: [项目/功能名称]
## 目标
## 技术栈
## 命令
## 项目结构
## 代码风格
## 测试策略
## 边界（总是/先问/绝不做）
## 成功标准
## 开放问�?```

### 将模糊需求重构为成功标准
```
需�? "让仪表板更快"
�?重构�? LCP < 2.5s, 初始数据加载 < 500ms, CLS < 0.1
```

### 约束
- 规格先行：代码之前必须有规格文档
- 假设浮出：不默默填充模糊需�?- 六领域覆盖：目标/命令/结构/风格/测试/边界
- 成功标准可测�?- 规格是活的：随决策和范围变化而更�?
<!-- /sub-mode: spec-driven -->

---

<!-- sub-mode: corecoder -->
## 子模式：CoreCoder核心实现（合并自corecoder v1.0.0�?
> 仅当用户明确要求CoreCoder模式/Claude Code核心模式时加载本节�?
### 核心理念
结构化编码代理行为，通过工具调用规范和安全规则确保代码质量�?
### 工具使用规范

| 工具 | 用�?| 示例 |
|------|------|------|
| read | 理解上下�?| read("src/main.py", offset=1, limit=50) |
| edit | 精确修改 | edit("src/main.py", old="x=1", new="x=2") |
| write | 创建新文�?| write("src/new.py", content="...") |
| exec | 执行命令 | exec("python test.py") |
| sessions_spawn | 子任�?| 复杂任务拆分 |

### 安全规则
1. **不删除文�?* �?只移动到_bak_
2. **不修改系统文�?* �?只在工作目录内操�?3. **危险命令需确认** �?批量操作前做dry-run
4. **记录所有修�?* �?写入memory日志

### 注意事项
- 优先使用edit而非write（保留文件历史）
- 大文件使用offset/limit分页读取
- 修改前先read理解上下�?- 复杂任务用子代理，避免主会话阻塞

<!-- /sub-mode: corecoder -->

---

<!-- sub-mode: implement -->
## 子模式：规划→TDD→审查串联（合并自implement v1.0.0�?
> 仅当用户要求完整实现串联/执行脚手架时加载本节�?
### 核心理念
将planning-and-task-breakdown、tdd、code-review三个skill串联，形成从任务拆解到高质量交付的完整实现链路�?
### 为什么组合？
- 直接编码容易遗漏边界条件
- 只做TDD不做审查，代码质量可能差
- 只做审查不做TDD，返工成本高
- 组合后：规划确保方向正确 �?TDD确保实现正确 �?审查确保质量达标

### 执行流程

**Phase 1: 任务规划（planning-and-task-breakdown�?*
1. 理解需求和验收标准
2. 将工作拆解为垂直切片
3. 建立依赖关系�?4. 为每个切片定义完成标�?
**Phase 2: TDD实现（tdd�?*
对每个任务切片：
1. **Red** �?写一个失败的测试
2. **Green** �?写最少的代码让测试通过
3. **Refactor** �?在测试保护下重构
4. 重复直到所有验收标准被测试覆盖

**Phase 3: 代码审查（code-review�?*
1. **Axis 1: Standards** �?代码规范、设计模式、可维护�?2. **Axis 2: Spec** �?需求对齐检�?
**Phase 4: 修复 + 验证**
1. 修复问题（回到Phase 2的Red-Green-Refactor循环�?2. 重新审查（Phase 3�?3. 直到审查通过
4. 执行/verification-before-completion

### 适用场景

| 场景 | 调整 |
|------|------|
| 新功�?| 完整执行Phase 1-4 |
| Bug修复 | Phase 1简化，Phase 2先写复现测试 |
| 重构 | Phase 1聚焦重构目标，Phase 2确保行为不变 |
| 小改�?| 可跳过Phase 1，直接Phase 2 + Phase 3 |

### 质量门控
- Phase 1�?: 任务列表已确认，每个任务有明确验收标�?- Phase 2�?: 所有测试通过，无failing test
- Phase 3→完�? 审查通过，无blocker级别问题

<!-- /sub-mode: implement -->

---

## 任务完成�?
完成任务后，做任务总结，将操作记录更新�?record.md 中�?
---

*Version 13.0.1 �?增加任务完成后更新record.md规则*
# AI 使用总规则

本文件是任务执行层规则，项目级规则以根目录 `AGENTS.md` 为唯一完整信源。两者冲突时，以 `AGENTS.md` 为准。

## 1. 使用顺序

本文件为按需读取的任务执行层规则总览，不要求每次任务都读取。项目级常驻入口以根目录 `AGENTS.md` 为准。

需要查看总规则、任务分级、workflow 映射或模板索引时，建议：

1. 阅读 `AGENTS.md`
2. 按需阅读本文件
3. 判断任务级别（1WEEK/3DAY/1DAY）
4. 阅读任务目录下的 `context.md`（如已整理）
5. 根据任务类型读取对应模板或 `ai-pilot/reference/workflows/` 下对应 workflow
6. 确认输入材料是否充分、是否脱敏

## 2. 快捷指令分层

### 核心治理指令

以下指令用于项目接入、任务建档和试点度量闭环，建议按流程执行：

- 初始化项目
- 开始任务
- 完成任务

### 按需能力指令

以下指令作为可选能力，不要求每个任务都执行，也不要求按固定顺序执行：

- 梳理需求
- 开始设计
- 编写测试用例
- 开始编码
- 执行测试
- 审查代码
- 生成阶段汇总

按需能力指令触发时，AI 只处理当前指令目标，不自动补跑整条任务链。如发现关键前置信息缺失，应说明风险并给出最小补充建议。

## 3. 任务分级使用原则

| 级别 | 适用场景 | 建议处理 |
|---|---|---|
| 1WEEK级 | >3天的新功能、架构变更或跨系统改造 | 建议整理完整 context，并按需使用需求、设计、测试、编码、测试执行、审查和完成任务 workflow |
| 3DAY级 | 1-3天的中等需求、接口开发或局部流程调整 | 建议整理精简 context，按任务阶段选择对应 workflow |
| 1DAY级 | <1天的 Bug fix、配置修改、文案调整或小范围重构 | 默认轻量处理，按需补充 context、测试记录或审查摘要 |

1WEEK/3DAY级任务建议先整理 `context.md`；1DAY级任务在问题上下文复杂、涉及缺陷系统、涉及多个文件或用户明确要求时整理。

## 4. 建议优先参考的模板

| 任务类型 | 模板 |
|---|---|
| 1WEEK级上下文任务 | `11-context-1week-template.md` |
| 3DAY级上下文任务 | `12-context-3day-template.md` |
| 1DAY级上下文任务 | `13-context-1day-template.md` |
| 需求类任务 | `01-requirement-spec-template.md` |
| 设计类任务 | `02-design-template.md` |
| 接口类任务 | `03-api-design-template.md` |
| 数据库类任务 | `04-db-design-template.md` |
| 测试类任务 | `05-test-case-template.md` |
| 代码审查类任务 | `06-code-review-template.md` |
| 上线说明类任务 | `07-release-note-template.md` |
| 使用记录类任务 | `08-ai-usage-record-template.md` |
| 试点评估类任务 | `09-poc-evaluation-template.md` |
| Prompt 协作类任务 | `10-prompt-guide.md` |
| 测试执行日志类任务 | `14-test-execution-log-template.md` |

## 5. workflow 映射

| 指令 | workflow |
|---|---|
| 初始化项目 | `ai-pilot/reference/workflows/00-init-project.md` |
| 开始任务 | `ai-pilot/reference/workflows/01-start-task.md` |
| 梳理需求 | `ai-pilot/reference/workflows/02-prepare-requirement.md` |
| 开始设计 | `ai-pilot/reference/workflows/03-prepare-design.md` |
| 编写测试用例 | `ai-pilot/reference/workflows/04-prepare-test-cases.md` |
| 开始编码 | `ai-pilot/reference/workflows/05-start-coding.md` |
| 执行测试 | `ai-pilot/reference/workflows/06-run-tests.md` |
| 审查代码 | `ai-pilot/reference/workflows/07-code-review.md` |
| 完成任务 | `ai-pilot/reference/workflows/08-finish-task.md` |
| 生成阶段汇总 | `ai-pilot/reference/workflows/09-generate-summary.md` |


## 6. 大型项目轻量使用原则

- 不默认全量读取 `src/`、`test/`、`docs/`、`config/` 或整个仓库。
- 优先基于任务编号、用户指定文件、错误日志、失败测试名、接口路径、路由、类名、方法名和配置项名称精确定位。
- 默认先读取最相关的少量文件；如变更清单包含更多文件，先读取文件清单和 diff 摘要，再分批深入。
- `开始任务` 只扫描配置文件、一级目录和任务关键词相关文件名，不默认读取业务源码全文。
- `完成任务` 按 1WEEK/3DAY/1DAY 分级简化，无法判断的量化数据填“待人工补充”。
- `生成阶段汇总` 只扫描 `ai-pilot/poc/` 下任务产物，不扫描业务源码或整个仓库。

## 7. 产物要求

| 级别 | 建议沉淀 | 可按需补充 |
|---|---|---|
| 1WEEK级 | context、全部核心任务文件、涉及测试时的 test-execution-log | 试点评估、专题复盘 |
| 3DAY级 | context、requirement、design、test-cases、涉及测试时的 test-execution-log、review-summary、ai-usage-record | api-design、db-design、release-note |
| 1DAY级 | review-summary、ai-usage-record | context、test-execution-log、其余按需 |

所有产物沉淀到 `ai-pilot/poc/{任务编号}/`。

## 8. 禁止行为

AI 不建议：

- 直接合并主干
- 绕过人工 Review
- 直接修改生产配置
- 直接执行生产数据库变更
- 输出密钥、密码、Token、连接串
- 使用未经脱敏的敏感业务数据
- 在不理解业务规则的情况下直接生成最终代码
- 把不确定内容当作确定结论输出

## 9. 输出要求

所有输出建议清晰标注：

- 输入依据
- 假设条件
- 修改范围
- 影响范围
- 风险点
- 需要人工确认的问题
- 测试验证建议

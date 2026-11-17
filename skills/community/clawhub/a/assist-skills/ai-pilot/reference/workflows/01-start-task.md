# 开始任务 workflow

触发词：`开始任务：{任务名称}`、`新建任务：{任务名称}`、`启动任务`、`创建任务 TASK-xxx，3DAY级，{任务名称}`

定位：核心治理指令。用于任务建档和任务产物初始化，建议按流程执行；大型项目中必须限制扫描范围。

## 执行步骤

1. 从用户描述中提取任务编号、任务名称和任务级别。
2. 如用户已提供任务编号或任务级别，优先使用用户提供的信息；缺失时再自动生成或建议。
3. 自动生成任务编号时，格式为 `TASK-{YYYYMM}-{序号}`。序号从 `ai-pilot/poc/` 已有任务编号中递增；如无法判断，从 `001` 开始。
4. 根据任务描述建议任务级别：
   - 1WEEK级：新功能、架构变更、跨系统改造，预计 >3天。
   - 3DAY级：中等需求、接口开发、局部流程调整，预计 1-3天。
   - 1DAY级：Bug fix、配置修改、文案调整、小范围重构，预计 <1天。
5. 向用户确认任务编号、任务名称和任务级别。
6. 用户确认后，在 `ai-pilot/poc/{任务编号}/` 下创建任务目录。
7. 根据级别从 `ai-pilot/standards/` 读取模板并生成任务产物：
   - 1WEEK级：`context.md`、`requirement.md`、`design.md`、`api-design.md`、`db-design.md`、`test-cases.md`、`test-execution-log.md`、`review-summary.md`、`release-note.md`、`ai-usage-record.md`。
   - 3DAY级：`context.md`、`requirement.md`、`design.md`、`test-cases.md`、`test-execution-log.md`、`review-summary.md`、`ai-usage-record.md`。
   - 1DAY级：`review-summary.md`、`ai-usage-record.md`；如用户要求或上下文复杂，再生成 `context.md`。
8. `context.md` 按级别使用不同模板：
   - 1WEEK级：`ai-pilot/standards/11-context-template.md`。
   - 3DAY级：`ai-pilot/standards/12-context-lite.md`。
   - 1DAY级：`ai-pilot/standards/13-context-mini.md`。
9. 每个文件预填写任务编号、任务名称、所属项目、日期、使用工具和任务级别。
10. 引导用户在 `ai-usage-record.md` 中补充 `预计人工完成工时（小时，不使用 AI）`，该字段为必填，用于完成任务时计算节省工时。
11. 生成 `README.md`，列出任务编号、名称、级别、产物清单和 context 补充建议。
12. 输出任务目录、已生成产物和下一步建议。

## 大型项目最小扫描规则

`开始任务` 不应默认全量扫描业务源码。自动扫描仅限：

- 项目配置文件，如 `package.json`、`pom.xml`、`build.gradle`、`pyproject.toml`、`go.mod`、`*.sln`。
- 根目录和一级子目录清单。
- 与任务名称、接口名、路由、错误信息、模块名相关的文件名检索结果。
- 明显相关的构建、测试、迁移或 schema 配置摘要。

默认不读取 Controller、Service、测试目录或业务源码全文。如确需扩大范围，应先说明原因、计划读取的目录或文件类型，以及预期验证的问题。

## context 引导

- 1WEEK/3DAY级任务建议补充 `context.md`。
- 1DAY级任务仅在上下文复杂、涉及多个文件、关联缺陷系统或用户要求时补充。
- 3DAY级 context 建议最低包含 3 条业务规则、1 条需求来源、2 个相关代码位置和明确测试口径。
- 未达到最低质量门槛时，提示用户补充，不要直接进入编码。

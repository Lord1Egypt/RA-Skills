# CLAUDE.md

本项目参与麟览（LINLAN）公司 AI 试点。

请优先阅读项目根目录的 `AGENTS.md`，并将其作为 AI 开发助手任务的主要使用参考。触发快捷指令时，先按 `AGENTS.md` 第 15 节映射读取 `ai-pilot/reference/workflows/` 下对应 workflow 文件。

根据任务类型读取 `ai-pilot/standards/` 下对应模板。如任务目录下已整理 `context.md`，1WEEK/3DAY级任务建议先阅读该上下文材料，1DAY级按需阅读。

支持快速指令：

- 核心治理指令：初始化项目、开始任务、完成任务
- 按需能力指令：梳理需求、开始设计、编写测试用例、开始编码、执行测试、审查代码、生成阶段汇总

按需能力指令只处理当前目标，不自动补跑整条任务链。大型项目中不默认全量读取 `src/`、`test/`、`docs/`、`config/` 或整个仓库。

使用安全提醒：

1. 开始任务前，建议先读取根目录 `AGENTS.md`。
2. 1WEEK/3DAY级任务在编码前建议读取并参考 `ai-pilot/poc/{任务编号}/context.md`；1DAY级如上下文复杂再读取。
3. 任务过程产物建议写入 `ai-pilot/poc/{任务编号}/`。
4. 请勿处理未脱敏数据，请勿硬编码密钥、Token、连接串或生产配置。
5. `执行测试` 和 `审查代码` 为按需能力，不强制每个任务执行；触发时应使用最小必要上下文。

文档输出建议使用中文。
不确定时建议先提问，不直接实现。

## 麟览公司典型技术栈

以下为麟览公司 AI 试点常见技术栈，供 AI 推理参考：

- Java Spring Boot (若依框架) + Vue3/Element Plus + MySQL + Redis
- Python Flask + Dashboard + MySQL/SQLite
- Python 脚本（数据处理、定时采集、代码生成）
- Maven 多模块项目 + MyBatis Plus
- Gitee 代码托管

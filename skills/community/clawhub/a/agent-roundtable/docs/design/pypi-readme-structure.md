# README / PyPI 展示结构建议

> 面向 `agent-roundtable` 首次 PyPI 发布的设计侧信息架构记录。目标是让用户打开 GitHub README 或 PyPI long description 后，10 秒内看懂价值、包名和最小用法。

## 首屏阅读路径

建议 README/PyPI 首屏按下面顺序组织：

1. Logo / 标题 / 一句话定位：先说明这是多 Agent 圆桌讨论引擎，不是聊天机器人或封闭编排平台。
2. Badge / 状态：只保留测试、License、Python 版本、零依赖等低噪音状态信息。
3. 10 秒速览：把 `pip install agent-roundtable` 前置，并用短表格说明“解决什么问题、包名与导入名、是否独立、是否可接框架、输出是什么”。
4. 什么时候用它：用 4 步解释会议协议层心智——创建会议、顺序发言、观察收敛、沉淀结论。
5. 快速开始：安装、源码安装、包名防误装说明、最小代码示例。
6. Feature / Integration / Architecture / Roadmap：放在 Quick Start 后，服务深度阅读。

## 本次已做调整

- 将原“30 秒理解 Roundtable”改为“10 秒速览”，减少首屏阅读负担。
- 将安装命令 `pip install agent-roundtable` 前置到首屏代码块，强化 PyPI 页面第一眼的行动点。
- 增加“包名和导入名是什么？”行，明确安装包名是 `agent-roundtable`，代码导入名是 `roundtable`。
- 增加“什么时候用它？”流程段，把产品定位转成用户可理解的 4 步使用心智。
- 保留饼哥已完成的 PyPI 包名说明和发布 checklist，不改变发布边界。

## PyPI Markdown 注意事项

- 避免依赖 GitHub-only 的复杂 HTML、折叠块或自定义样式；PyPI 对 HTML 会做安全过滤。
- 表格保持简单二维结构，避免嵌套列表或复杂 HTML。
- 代码块使用标准 fenced code block，语言标记使用 `bash` / `python` / `yaml`。
- 图片使用绝对 URL；相对链接在 PyPI 上可能无法按 GitHub 语义解析。
- 安装命令统一写作 `pip install agent-roundtable`，不要引导用户安装 `roundtable` 或 `roundtable-ai`。

## 发布前设计侧验收

- [x] README 首屏 10 秒内能看到包名、价值和用途。
- [x] 安装命令使用 `pip install agent-roundtable`。
- [x] Quick Start 保留创建讨论、发言、状态、总结、结束讨论的完整路径。
- [x] 表格、引用块、代码块均使用 PyPI 友好的 Markdown 写法。
- [x] 保留发布 checklist 与“不要今天发布 PyPI/TestPyPI”的边界。

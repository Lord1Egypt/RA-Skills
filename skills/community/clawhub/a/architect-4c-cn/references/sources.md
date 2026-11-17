# 来源与示例约定

核对日期为 2026-11-04。C4 模型由 Simon Brown 提出。

## 官方依据

- [官网首页](https://c4model.com/)列出分层抽象、分层视图、补充视图，以及记法和工具独立性。
- [抽象](https://c4model.com/abstractions)定义系统、容器、组件与代码元素的包含关系。
- [图类型](https://c4model.com/diagrams)说明四层静态结构、补充视图与选图建议。
- [记法](https://c4model.com/diagrams/notation)说明元素、关系、标题和图例的要求。
- [Mermaid C4 文档](https://mermaid.js.org/syntax/c4.html)说明原生语法与布局能力。

主技能的官网原则概述以上说明。各视图参考另附对应的官方定义。

官方站点与示例图采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。本技能使用自行编写的文字和支付平台示例。

## 技能参考

[softaworks 的 c4-architecture](https://github.com/softaworks/agent-toolkit/blob/main/skills/c4-architecture/SKILL.md)提供工作流和语法参考。层级定义以 C4 官网为准，Code 是第四层。

## 示例约定

六类模板共用一个虚构支付平台。商家订单系统和支付渠道在外部，平台内部包含支付应用和支付库。后台任务是应用内的组件，代码图只展开支付处理。

幂等、原子通知任务、结果核实、任务租约和重试边界是示例设计。部署图中的两个应用实例与单个数据库用于说明映射关系。实际使用时按项目资料核对。

[绘图与视觉规范](diagram-guidelines.md)由本技能独立维护。

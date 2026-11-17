# 参考文档路由

入口是 `routing-index.md`（按问题选文件）；本文件只说明 references 与 docs 的分工。

- `generic-playbook.md`：六类膨胀源的识别信号、手法、保体验红线、常见反模式。
- `measurement.md`：三本账、怎么测常驻、同类任务对比、换算公式、报告模板。
- `context-model.md`：六类源到 Hot/Warm/Cold 的对应，以及 Token/磁盘账本口径。
- `case-workbuddy.md`：一次真实瘦身的落地过程与逐块数字（参照物，不是前提）。
- `adapter-contract.md`：宿主适配器的最小接口、能力和三种接入方式（布局描述 / 内置分支 / 纯手工）。
- `integration-routing.md`：Ponytail、Skill Architect、Memory Orchestrator 和发布流程的归属、交接数据与降级规则。

`docs/` 保存产品级架构、安全和验收；`references/` 只放需要按需读取的细化说明。不得在这里复制 Memory Orchestrator 的阈值或 Ponytail、Skill Architect 的执行算法。

- `../docs/audit-json-contract.md`：只读审计的稳定 JSON 字段、退出码和读取边界。

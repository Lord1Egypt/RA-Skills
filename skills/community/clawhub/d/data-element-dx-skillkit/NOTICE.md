# NOTICE — 上游项目归属与许可证

本套件（data-element-dx）采用 **Apache License 2.0** 授权。
部分能力在设计上融合了以下开源项目的方法论（均已在对应 SKILL.md 的 `metadata.fused_from` 中标注）：

| 来源项目 | 许可证 | 融合内容 | 落点 |
|---|---|---|---|
| data-governance（skillkit.io 实现） | Apache-2.0 | 数据目录、血缘、质量规则、stewardship | dx-data-quality |
| cbrock84/headcount — data-governance | 见上游仓库 | 指标字典（Metric Dictionary）、具名 Owner、质量"实测而非宣称"、默认开放访问 | dx-data-quality |
| omer-metin/skills-for-antigravity — data-governance | Apache-2.0 | 参考模式（patterns/sharp_edges/validations）组织结构 | dx-data-quality |
| DKSang/DES-SKILL — des-governance-and-security | 见上游仓库 | RBAC/RLS、PII 分类、保留期与删除、审计日志、HALT 停机卡口 | dx-architecture-opt |
| csv-data-wrangler | 见上游仓库 | 按数据规模选择工具（pandas/Polars/DuckDB/Spark）决策树 | dx-data-baseline |
| duckdb/duckdb-skills | 见上游仓库 | DuckDB 直查文件做表画像 | dx-data-baseline |
| borghei — data-analyst | 见上游仓库 | What / So What / Now What 分析叙事框架 | dx-application-plan |

方法论部分（七道工序、DCMM 对标、数据要素政策索引、交付编排）为本项目原创，以 Apache-2.0 授权。

> 说明：本套件未直接复制上述项目的代码或文本，而是吸收其方法论并结合中国国资/集团场景重写。若上游权利人认为存在不当引用，请联系调整。

本套件**不包含任何真实客户数据**。`cases/` 目录仅提供接口规范与脱敏模板。

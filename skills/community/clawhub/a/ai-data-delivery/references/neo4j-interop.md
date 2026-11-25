# Neo4j / Ontology Graph Spec 离线互通

**v0.3.2 增加另一条 CSV/Cypher 数据导出路径**：[只读元数据与 Neo4j 导出](readonly-metadata.md)。下面的 `database_import_ready=false` 只描述 OGS 设计投影，不描述新的实际数据导入包。/ v0.3.2 adds a separate importable CSV/Cypher path. The OGS limits below continue to apply to design exchange only.

需要把已核对的业务对象交给图建模工具时使用本页。`model.json` 仍是唯一语义定义；OGS 是从固定语义包生成的只读投影，不建立第二份手工维护本体。

## 导出与检查

输出目录须已存在，文件不覆盖。指令不连接数据库、不执行 SQL/Cypher，也不回写工作台。

```powershell
python -X utf8 scripts/ontology_export.py --package "./delivery/semantic.zip" export --out "./delivery/model.ogs.json" --report "./delivery/model.coverage.json"
```

目标是 **OGS 格式 1.1.0**，不是库版本号。导出器本身不包含官方 SDK，报告 `official_library_validation: not_run_by_exporter`。将文件交给支持此格式的官方库，分别检查 core、labelled、consistentSchema、mappable 等适用规则；“结构有效”不等于“映射齐全”或“实际数据满足约束”。不能把 `ALL` 通过作为普通业务草稿的默认门槛。

从工具实际导出回 OGS JSON 后检查：

```powershell
python -X utf8 scripts/ontology_export.py audit --original "./delivery/model.ogs.json" --returned "./delivery/tool-returned.ogs.json"
```

退出码：`0` 已导出或本投影及载荷保持一致，`1` 往返发现变化或丢失，`2` 输入、读取或写入失败。审计分别报告原生节点关系和业务语义/来源是否保留；文件能打开不能替代往返检查。`audit` 只比较本导出器生成的有限投影，不证明任意 OGS 文档逻辑等价。

## 映射约定

| 原语义 | OGS 表达 | 仍须注意 |
| --- | --- | --- |
| 已确认业务对象 | `nodes`，原稳定 ID 作键；定义作 description、业务名称/别名作 aliases | 自动生成的 `ADD_...` label 标记为 `new_design_identifier`，用于新图设计；不声称与已有库 label 匹配。 |
| 已确认显式 business 关系，两个端点均为已确认对象 | `relationships` 和原方向，稳定生成 type | 不从外键推导业务关系，不推断反向责任、基数或继承。 |
| 已确认 has_attribute 指向已确认属性 | 对象的 `properties` | 只映射明确的受支持值类型；如 decimal 的精度不能转换为 FLOAT，则保留原定义并报告未映射。属性名同样是新设计标识。 |
| 规则、指标、分类、物理表/字段/映射、适用范围、有效期、身份、依据等 | `extensions.custom.ai_data_delivery` 的 `model_json`、`sources_json` | OGS 对这些业务含义没有约定，第三方工具不会自动理解或执行。 |
| 草稿、待复核、停用内容 | 同一自定义载荷，保留状态；不投影成已确认原生结构 | 固定语义包是否完整、是否草稿在报告中保留。 |

长于原生 description 限额的定义会在原生字段截取并逐项告警，完整内容仍在载荷。所有语义资产都有覆盖记录，不把指标或规则伪装成业务实体来凑完整图。未明确的业务键、复合租户身份、关系基数、查询和数据源映射不自动生成。

自定义载荷保存规范化 JSON **字符串**及 SHA256，避免 JavaScript 数值转换破坏长账号、零/假/空值等类型。载荷包括包内引用的来源摘录，不额外读取原附件。该副本只供机器读取与往返审计，修改业务定义应返回工作台生成新快照。摘要不是签名，不能证明来源可信。

## 交付界限

OGS 原生结构保留下来，也可能同时丢失自定义载荷。经过 Aura `data_model` 等转换时尤其要检查真实返回文件；不可把格式迁移支持写成无损导入或已连接数据库。本版本未自动生成 source tables/mappings、约束或导入脚本；`database_import_ready` 始终为 `false`。

2026-11-12 本地实测：npm `@neo4j/ontology-graph-spec@0.10.0` 读取本导出的 1.1.0 格式报不支持的迁移；固定为 `0.12.0` 后，交通、农业、高校、金融四个合成案例的 core、labelled、consistentSchema 检查均无问题。OGS JSON/YAML 往返保留自定义载荷，四个 YAML 返回文件审计均为 `preserved`；经 Aura `data_model` 格式往返的四个案例均丢失本工具的命名空间及别名等内容，审计均报 `changed_or_lost`。这是特定版本和样例的离线文件实验，未启动 Aura 服务或导入 Neo4j 数据；也不证明真实源映射已齐全。四域样例不含显式属性归属，属性类型另用合成边界测试覆盖。

属性边界实测还发现：SDK 的 consistentSchema 要求显式属性 `name`，导出器已将生成的属性标识同时写为 `name`。未映射的 `decimal(20,2)` 不会擅自改成 FLOAT 或 ANY；含此未知类型的样例经 Aura 格式转换会明确拒绝转换，必须先由建模者确认适当表示，不能为通过转换牺牲精度含义。

实际 Neo4j 集成还需要明确实际标签/属性、复合身份、物理源映射、查询权限及运行环境。OGS 模型声明本身不证明端点、基数、枚举、规则或租户授权已被数据库执行。Agent 问数仍使用固定语义包读取上下文，再由获授权的执行器查询；OGS 导出不代替问数执行。

官方依据（核对日期 2026-11-12）：[1.1.0 JSON Schema](https://neo4j.com/docs/ontology-graph-spec/1.1.0/schema.json)、[项目与库](https://github.com/neo4j/ontology-graph-spec)、[扩展约定](https://github.com/neo4j/ontology-graph-spec/blob/main/docs/modules/format/pages/reference/extensions.adoc)、[迁移说明](https://github.com/neo4j/ontology-graph-spec/blob/main/docs/modules/libraries/pages/migration.adoc)。格式版本与 SDK 版本须分别固定并实测；不能仅以 GitHub release 标签推断 npm 包的可读格式。

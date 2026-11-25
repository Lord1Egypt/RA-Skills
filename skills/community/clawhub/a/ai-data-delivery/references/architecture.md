# Architecture / 架构与取舍

## 从要完成的事出发

一个接收方要可靠地使用业务知识，至少要知道：对象是谁、规则在什么范围成立、依据来自哪里、哪里仍未知，以及资料变化后旧结论是否还能使用。图形、命令和文件格式都是服务这件事的手段。

产品定位是可用完即走的本地工具，主链是导入结构、按需编辑、导出／读取。CLI 为主，可视化是同一模型的临时编辑入口；不引入账号、工作空间管理或常驻 Agent 网关。

因此本工具保留一份带稳定身份与证据的语义图谱。可选业务问题是它的消费者，交付包是它的固定投影；界面和宿主不能各自维护一套业务事实。图谱可视化帮助专业维护，但不是用户开始工作的前置条件。

## 四类职责

| 承担方 | 负责什么 | 不应代替什么 |
| --- | --- | --- |
| 业务人员 | 提出问题，判断影响结果的业务歧义，核对依据 | 不承担 ID、JSON、重试协议等技术操作 |
| 宿主 Agent | 理解材料，发现可复用定义，提出带依据的候选，调用已授权工具 | 不把推断或词法匹配写成已确认事实 |
| 本地知识服务 | 保存来源、维护身份与修订、核对候选、计算依赖与失效、生成交付包 | 不充当大模型或生产业务执行器 |
| 接收 Agent / 应用 | 读问题与定义、按需取证、判断缺口；另行使用已授权的数据/动作接口 | 不把包完整当成答案正确或执行许可 |

## 实现对应

| 层 | 主要实现 | 约束 |
| --- | --- | --- |
| Skill 入口 | `SKILL.md`、按需 `references/` | 保留会改变判断的约束，条件性细节按需读取 |
| 材料与维护 | `workbench/knowledge.py`、parsers、store、metadata_service | 共用修订、回执、证据和已有处置；不绕过服务直接改库 |
| 问题与影响 | `scenario_contract.py`、`query_control.py` | 从同一资产派生，不另存可漂移的控制真值 |
| 交付与读取 | `semantic_package.py`、`scripts/semantic_read.py` | 已发快照不随项目变动；`brief` 组合现有 task/context/control，不发明新执行状态 |
| 操作界面 | `knowledge.js`、`scenarios.js`、`query-bindings.js` | 显示业务含义并使用相同写入路径；表单核对仍是人的观察，不是自动等价证明 |
| 可选互操作 | 目录连接器、Neo4j/OGS 导出、旧数值工具 | 显式选择；不成为本体建模必装依赖，不静默同步旧模型 |

## 最短链路的实现

- `knowledge.py import --seed-draft` 或 `scan --seed-draft` 仅初始化空图，保存有来源的表、字段与外键草稿；不能伪造人工确认。已有图使用原候选差异路径。
- `start.py --project` 只在需要可视化时运行。默认图谱且自动选择结构视图，顶部三个入口；来源、候选和历史可按需展开。
- `knowledge.py export` 复用原发布与依赖闭包，无业务问题、HTTP 服务前置条件；默认导出全部有效资产，也可明确选择 ID。草稿需要 `--draft`，确认导出继续执行原保护。
- `semantic_read.py` 在独立进程读取固定包，返回 JSON。编辑器可关闭。没有新建 MCP、生产 API 或第二套模型。

## 本轮结构检查的结论

- **保留统一事实源与事务。** 它们防止人工修正被覆盖、规则漏带和旧核对继续显示有效；不能为了少点击而删除。
- **缩短入口，细节留在合同。** 根 Skill 负责路由和关键不变量，README 负责让潜在用户理解价值并完成首次体验；历史信息放到 Changelog 和版本参考。
- **合并接收操作，不复制数据。** 新 `brief` 直接复用已有读取方法，保留分页、证据省略、旧包和执行限制。
- **将技术结构转为可读核对。** 指标已有单数据集绑定时，用字段名称、统计方式、过滤值类型、时间与原文核对。表单不支持的复杂表达式保持原样，交回宿主补充候选。
- **按实际问题改善检索。** 问题候选原本已有别名与 Unicode 规范化；本轮统一普通搜索的规范化，并显示匹配依据。没有凭空引入同义词、向量服务或置信度。
- **有界保留旧工具。** 历史数值路径仍有消费者，保留明确入口；不为缩减文件数破坏旧用法。文件存在不等于每次加载，入口不要求预读全部参考。

## 使用成本与尚未证明的效果

本轮直接可检查的变化是：直接可编辑的结构草稿、CLI 导出、按需图谱，以及可选问题包的一次读取与口径表单。它们不自动证明任务成功率、业务准确率或耗时改善。

验证分为程序回归、浏览器操作、独立 Agent 合成任务和真实用户/业务验收。前三类结果见[0.3.6 验证](https://github.com/franklinxkk/ai-data-delivery/blob/v0.3.6/references/v0.3.6-release-validation.md)；本轮没有把它们替代第四类。未来应在同一材料与预期下比较错误、漏条件、澄清次数、人工介入和总耗时，避免仅以文档长度或测试数量判断价值。

## English summary

CLI-first import → optional graph editing → export/offline reading. One evidence-linked semantic graph is authoritative. Questions reference it; packages and query controls are derived. The host reasons, the operator reviews business meaning, the local service preserves identity/evidence/revisions, and the recipient consumes context before separately authorized execution. `brief` composes existing readers; the binding form updates the original metric through the existing service. Legacy numeric tools remain separate. Shorter instructions and fewer entry operations are measured changes, not proof of user productivity or semantic accuracy.

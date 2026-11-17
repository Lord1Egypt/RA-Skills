# 从指标到明细，再交给 Agent

适用：已经声明了单表指标，想解释数值、选择相关语义或检查消费者是否仍使用同一份模型。先核对业务定义，再执行。工具不理解自然语言，也不实现生产鉴权。

## 一次跑通

在仓库根目录执行；输出目录需为空，示例全部是合成数据：

```bash
python examples/conference-practice/run_demo.py --out tmp/conference-demo
python scripts/query_bundle.py --model tmp/conference-demo/traffic.yaml --db tmp/conference-demo/traffic.sqlite --metric distinct --columns company_id --out tmp/metric-detail.json
python scripts/select_context.py --model tmp/conference-demo/traffic.yaml --metric distinct --columns company_id --out tmp/agent-context.json
python scripts/select_context.py --model tmp/conference-demo/traffic.yaml --check tmp/agent-context.json --out tmp/context-check.json
```

`query_bundle` 返回数值、符合范围的记录数、当前页明细、分页信息及模型/快照指纹。默认每页50，`--limit 1 --offset 1` 查看另一页；数值仍按完整范围计算。声明主键缺失、重复或含NULL时拒绝，防止分页漂移。`--expected-model` 可传当前模型**文件**SHA256，失配不查询。库函数同名参数使用规范化JSON摘要，报告的 `model_hash_kind` 标明口径，不能混用。

明细是指标过滤后的输入记录，不等于 COUNT(column) 实际计入的非空项、COUNT(DISTINCT column) 的去重项或比率分子的记录。示例 A、A、NULL：记录行数3、非空计数2、去重非空计数1，输入明细始终3条。显示列没有过滤字段时仍先过滤再投影。

支持范围沿用现有单表 count/sum/avg/min/max/ratio。聚合外混入裸字段、未知列、多参数MAX/MIN、子查询或跨表表达式拒绝；不猜业务粒度。跨表先用 `check_join_graph` 检查路径，在目标引擎/受检视图中实现，再独立对拍，不能用 SUM(DISTINCT 金额) 通用消重。

## 工作台路径

1. `python -m workbench.serve --project tmp/my-project`，打开打印出的本机地址。
2. “数据与资料”导入模型和对应SQLite快照，样本来源选“合成/Mock”。
3. “检查与试算”→“指标与明细核对”选指标及返回字段，可选填写独立预期JSON。点击执行后查看数值、符合条件记录数、明细与证据。
4. 同一处点击“查看供 Agent 使用的上下文”。CLI命令可把同一选择保存为文件交给Agent。页面预览不意味着已调用外部Agent。
5. 修改指标或来源后重新检查；旧执行证据标过期。刷新页面可从历史证据重新打开结果，交付ZIP保留证据。

预期JSON示例：`{"metric_value":1,"matched_row_count":3,"detail_rows":[["A"],["A"],[null]]}`。只填数值会漏掉范围错误，故此入口同时核对三项。未填预期只标 `computed_only`；前后两条由同一编译器生成的查询相等，不构成独立业务验收。

## 上下文到底包含什么

`select_context` 只选择指定指标、其表达式/过滤/时间依赖、明细字段、声明主键与tenant字段；带对应对象的证据摘要。省略其他表、指标及本体关系。它是供Agent阅读的**片段**，不是完整模型，也不能拿来证明完整图查询。保留原 `model_inferred / owner_confirmed` 等等级，绝不因生成成功自动确认。

包内包含选择请求、主模型指纹、内容指纹、来源路径和摘要；`source_mode=snapshot`。`--check` 用当前模型重新选择并比对，模型变化返回 `CONTEXT_STALE`，内容改写或失效引用返回 `CONTEXT_INVALID`，退出码2。检查通过仅为 `matched`，不是业务验收pass。当前实现对主模型任何变化均保守失效；没有实时监听外部数据库。

包中的URL只是引用，本工具没有抓取链接正文。裁剪不是权限校验或脱敏，描述中仍可能有业务信息。接收方先获实际授权，再选择文件；生产服务每次执行仍需身份、行列边界、撤权检查。不能把role字段、tenant过滤或MCP入口当作权限实现。

## 消费失败与变更恢复

工作台“现有问数引擎”先读取 `/api/model`。来源表、tenant字段、指标表达式、过滤、连接键等已知投影不一致时不发送 `/api/ask`。兼容同义键的snake_case/camelCase表示；冲突表示拒绝，不静默选一个。此适配器只面向已有Java演示接口，完整本体等扩展能力仍未证明被消费。

显式status只认 `ok/success/completed/done`；旧接口无status时按原结果协议处理。拒绝、error、success=false、pending或未知状态即使带预期数值，也不能核对通过。NULL结果与没有结果区分。生产异步接口必须由适配器解释“受理/完成/失败”，不能泛用这组状态词。

CLI 消费者核对使用同一完成条件：`running/processing` 等未识别状态不能因数值相同而通过。无 status 的旧协议仍支持明确 value 或 rows；`rows=[]` 是空结果，`rows=[[null]]` 是包含 NULL 的结果。仅有 `value:null` 时，需要成功 status 或已返回 SQL 证明执行完成，不能将 `{}` 或字段全缺/全为 null 当作结果。计划稳定性检查可单独使用非空 SQL，但没有计划及实际结果证据时不能宣称稳定；预期拒答的用例仍按独立拒答条件判断。

字段移除或改名后先运行 `check_model --drift`；已结构化且属于本工具支持语法的指标，其表达式、过滤、分母依赖失效会报告。修正明确映射再重新生成上下文和执行证据，不按列位置自动替换，不复用旧成功数值。

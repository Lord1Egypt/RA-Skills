# 工具入口

以下命令在仓库根目录执行，完整参数用 `python scripts/<name>.py --help` 查看。除特别说明外不自动访问外部系统；带 endpoint 的工具会访问指定服务。`_*.py` 是内部共享模块，不是 CLI。

## 按角色找工具（先看这个，不用遍历命令清单）

| 角色 | 你的主干 | 快速通道 | 其余命令 |
| --- | --- | --- | --- |
| FDE 工程师 | 一个业务问题＋已有资料→start工作台或Agent代办→结果与消费核对 | [quickstart-fde](quickstart-fde.md) | 用到再查 |
| 数据产品经理 | 对Agent描述问题→核对包含与排除→看数值与明细 | [quickstart-pm](quickstart-pm.md) | 不用看 |
| 信息中心 | profile_db → check_consistency → check_constraints → gaps.yaml 闭环 | [quickstart-infocenter](quickstart-infocenter.md) | 不用看 |

> 注意 `--out` 语义：多数命令是**目录**；`detect_isomorphic.py` / `profile_db.py` 是**文件路径**。
> `impact_analysis --target` 写裸名（不带 `dataset:` 前缀）。端点类工具默认仅本机/内网，远程加 `--allow-remote`。

| 阶段 | 命令 | 作用与边界 |
| --- | --- | --- |
| 首次使用 | **start** | --project 新目录 --demo；或 --model/--ddl 加可选 --sample；准备并打开本机工作台，已有项目不覆盖 |
| S0 | derive_ontology | 已有数据集与显式关系生成本体候选；`--out` 为新文件，不覆盖已有语义或推断业务规则 |
| S0 | ingest_ddl | DDL 台账；可选 --model-out 部分草案，需核对解析范围 |
| S0 | profile_db | SQLite 数据画像；敏感名启发式不等于完整脱敏 |
| S0 | detect_isomorphic | 同构表候选，不自动决定合并 |
| S0 | harvest_metrics | 指标公式盘点，分类结果需结合真实来源复核 |
| S0 | gold_seed | 评测骨架，独立期望需补充 |
| S1 | **guide_model** | init/status/propose/apply/export，持久缺口与确认闭环 |
| S2 | propose_dws | 宽表设计草案 |
| S2 | gen_metadata | metadata 草稿，待确认项不能当事实 |
| S2 | bind_metrics | 指标与数据集绑定候选 |
| S2 | coverage_check | 模型/指标/用例覆盖检查 |
| S2 | gen_eval_cases | 扩展用例草稿，不生成可信业务金标准 |
| S2/S3 | check_model | 结构、引用、指标定义 lint |
| S3 | **check_join_graph** | --model [--db] --out；显式键与具体查询路径的粒度风险 |
| S3 | **check_constraints** | --model --db --out；六类规则，全量 SQLite 快照 |
| S3 | gold_lint | 用例集自身矛盾检查 |
| S3 | run_eval | live 或离线回归；--model/--db 绑定证据，模拟数据加 --mode mock |
| S3 | reconcile_paths | 单表指标直算；有 endpoint 才进行双路径对账 |
| S3 | **query_bundle** | --model --db --metric --columns --out；同快照的指标与输入明细，显式分页与模型/数据指纹；不是鉴权 |
| S4 | **select_context** | --model --metric [--columns] --out；选择指标及依赖；--check 核对已有包，失配拒绝，不自动读取外部链接 |
| S3/S5 | capture_case | 请求/SQL/结果取证卡；注意报告可能有敏感数据 |
| S3/S5 | ingest_feedback | 用户反馈归集 |
| S3/S5 | suggest_card | 修订建议卡，不自动授权修改 |
| S3/S5 | patch_model | syn/struct/set/batch/fixuid 五入口；batch 一次写入 ops.yaml，--db/--expect 验算作用见入口说明 |
| S4 | promote_draft | 盘点指标 → ✅/🔶/⛔/📋 四分提升草稿 + ops.yaml + 提升清单.md；草稿必须人审后 batch 合入 |
| S3/S5 | promote_gold | 已确认反馈加入评测集 |
| S4 | release_gate | --profile static/validated/production；默认不再跳过必需证据 |
| S4 | gen_dictionary | 由模型生成可读口径字典 |
| S4 | export_exchange | 模型/用例/证据/视图与哈希清单；输出目录必须为空 |
| S4 | **visualize_model** | --model [--session] [--report ...] --out model.html；离线只读视图 |
| S5 | check_consistency | 模型与物理结构漂移，不验证业务数据/时效 |
| S5 | plan_stability | 指定服务的重复请求抽查；SQL 指纹不同需解释，结果兜底不证明 SQL 计划一致 |
| S5 | impact_analysis | 文本引用得到影响候选，不是完整调用图 |
| S5 | probe_model | 检查目标服务当前模型信息 |
| S5 | rebuild | 触发目标服务重建，需在用户授权的范围内运行 |

## 本地可视化工作台

适合 FDE 和数据产品从结构与业务问题开始、不希望手写 YAML 的日常建模：

```bash
python scripts/start.py --project ./workbench-projects/my-project
```

工作台绑定本机回环地址。打开终端打印的网址后，可导入 DDL/模型/SQLite 快照，编辑图上的本体对象、关系、数据集、字段、指标、模板和约束，记录补齐答案与依据，运行检查和单表试算，查看版本并导出交付包或完整项目备份。拖动画布只改布局，不产生语义模型版本。

它复用 `check_model`、`check_join_graph`、`check_constraints`、`_sql.compile_single` 和 DDL 解析器。消费者检查只对接明确指定的已知本机 Java JSON 接口。当前不执行自由 NL2SQL、办事写操作、政策裁决或决策优化；场景编辑页会呈现所需条件与尚未接入的运行能力。细节见 [workbench README](../workbench/README.md)。

维护命令：`python -m unittest discover -s tests -v`、`python mocks/run_mock.py --all`、`python examples/onboarding/run_demo.py --out tmp/demo`、`python maintainer/build_skill.py --out dist`。验证强度不同，不能用一个命令的成功代替全部阶段。

报告传递：`export_exchange --report` 要求对象含 `evidence` 模型摘要和时间。`reconcile_paths --out` 是原始逐案结果列表，不能直接作验收报告导入；使用 `run_eval --help` 按独立预期、实际结果和模型绑定产生报告。

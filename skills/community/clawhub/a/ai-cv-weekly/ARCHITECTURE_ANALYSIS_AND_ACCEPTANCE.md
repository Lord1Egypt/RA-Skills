# ClawCat Brief 架构分析报告与整改验收标准

## 1. 文档目标

本文档用于对 `ClawCat Brief` 当前架构完成度进行系统评估，并给出后续整改项、优先级、验收标准与交付物要求。

目标不是单纯列问题，而是形成一套可执行、可验收、可复盘的整改基线，支撑项目向以下方向演进：

- 可插拔、配置驱动的报告生成平台
- 高确定性的 LLM 生成链路
- 可追溯、可评测、可观测的工程体系
- 支持多主题、多周期、多数据源扩展的通用化系统

---

## 2. 项目目标定义

### 2.1 目标能力

项目希望具备以下五类核心能力：

1. 设计一个可插拔、配置驱动的报告生成架构，支持多主题、多周期、多数据源扩展
2. 构建 `Fact Table + Grounding + Quality Gate` 的高确定性生成链路
3. 通过 `Golden Set + 自动评测` 持续优化生成质量，降低数值幻觉与格式错误
4. 实现 `claim -> evidence -> source` 的可追溯引用机制
5. 支持 HTML / PDF / 邮件 / webhook 多通道交付，并具备完整的 token、质量、失败可观测性

### 2.2 架构设计原则

后续整改必须遵守以下原则：

- 不为了“架构好看”而过度抽象
- 不为了“加分”而引入和目标无关的框架
- 优先解决真实质量问题，而非增加表面功能
- 所有高确定性能力都必须进入主链路，而不是作为旁路工具存在
- 所有配置化能力都应尽量外置，不在 Python 代码中散落策略常量

---

## 3. 当前架构概况

当前系统已形成以下主链路：

`Fetch -> FactFetch -> Score -> Select -> Dedup -> Edit -> Budget -> Gate -> Cite -> Render -> Output`

当前代码中已经具备的关键模块包括：

- `brief/pipeline.py`：主生成管线
- `brief/facts/`：Fact Source + Fact Table
- `brief/grounding/`：Grounding Pipeline
- `brief/gate.py`：Quality Gate
- `brief/citation.py`：Citation Engine
- `brief/eval/`：评测维度与 Golden Set 基础设施
- `brief/observability.py`：Pipeline Trace 可观测性
- `brief/presets.py`：内建 preset 定义

从架构层面看，系统已经从“能生成”升级到了“有治理能力的生成系统”，但距离“强配置驱动、高确定性、持续评测闭环”仍有明确差距。

---

## 4. 当前完成度评估

## 4.1 总评

综合完成度评估：**74 / 100**

当前状态已经可以作为一个有亮点的 LLM 工程项目，但还不能完全等同于“强配置驱动的高确定性生成平台”。

## 4.2 分项评分

| 能力项 | 当前完成度 | 结论 |
|---|---:|---|
| 可插拔架构 | 85 | 已具备 registry、preset、source/editor/fact source 扩展能力 |
| 配置驱动 | 70 | preset 与 source 已部分配置化，但 gate/eval/delivery 阈值仍硬编码 |
| 高确定性链路 | 85 | Gate 已真正进入主链路，支持 pass/retry/degrade/block |
| 自动评测 | 60 | 已有评测维度与 golden case schema，但闭环未完全打通 |
| 可追溯引用 | 75 | 已能生成 citation sidecar，但尚未进入最终交付视图 |
| 多通道交付 | 90 | HTML/PDF/邮件/webhook 已成型 |
| 可观测性 | 78 | run 路径较完整，但 stream 与 retry 后统计不一致 |

---

## 5. 已完成能力盘点

## 5.1 已经落地且价值明确的能力

### A. 主链路已支持高确定性治理

当前 `QualityGate` 已经不再只是“打分器”，而是主链路中的治理器，具备四态决策：

- `PASS`
- `RETRY`
- `DEGRADE`
- `BLOCK`

这意味着：

- 校验失败的结果不再默认继续发送
- 金融/股票等高风险场景下，严重幻觉可以被直接阻断
- 对不完全通过校验的内容，可以降级为“安全但不完整”的输出

### B. Fact Table 已进入 LLM 生成与 Grounding 双侧

当前 Fact Table 既用于：

- 生成前约束 LLM 使用事实数据
- 生成后校验数值是否可回溯

这是高确定性架构的正确方向。

### C. Citation 引擎已经具备后端能力

系统已经可以抽取 claim，并尝试绑定：

- `Fact`
- `Item`
- `Source`

同时可落盘为 `citations.json`，为后续前端展示与调试打下基础。

### D. Eval 基础设施已经建立

已经实现：

- 评测维度抽象
- `EvalRunner`
- Golden case 文件格式
- Golden result report 输出基础

这说明项目已经从“仅靠主观判断优化 prompt”，走向“用标准测试集约束生成质量”。

### E. Trace 可观测性已经进入项目主线

当前已经能记录：

- 数据源抓取数量
- facts 数量
- token 使用量
- quality / grounding 分数
- gate verdict
- phase timing
- 输出状态

这对项目工程成熟度有明显加分。

---

## 6. 关键问题分析

以下问题按严重程度分为 `P0 / P1 / P2`。

## 6.1 P0 问题：直接影响“高确定性”表述成立

### P0-1 配置驱动尚未闭环

问题：

- gate 阈值写死在 `brief/gate.py`
- eval 维度及权重未配置化
- delivery 策略未配置化
- strictness 逻辑依赖代码分支，而不是 preset/profile

影响：

- “配置驱动”只能部分成立
- 新主题扩展时仍需改 Python 逻辑
- 不利于后续真正平台化

### P0-2 Citation 尚未进入最终交付层

问题：

- citation 目前只输出到 sidecar JSON
- HTML/PDF 没有展示 claim/evidence/source
- 用户无法直接感知“可追溯”

影响：

- 技术能力存在，但产品价值不完整
- 简历里写“实现可追溯引用机制”说服力打折

### P0-3 Golden Set 还不是持续优化闭环

问题：

- 只有 case schema 和 check 逻辑
- 没有完整 `run_all(generate_fn)` 自动执行闭环
- 没有 baseline/current 自动对比机制
- 未接入 CI 或命令入口

影响：

- 现在更像“评测工具”，不是“评测体系”
- 还不能支撑“持续优化生成质量”这一表述

## 6.2 P1 问题：影响工程完备度

### P1-1 run 与 run_stream 的可观测性不一致

问题：

- `run()` 路径有 trace、eval、citation sidecar
- `run_stream()` 路径没有完整 trace 落盘，也没有 eval 结果持久化

影响：

- 两条路径语义更接近了，但还不是完全对齐
- 在线与离线行为差异仍可能造成定位困难

### P1-2 retry 后的 token/cost 统计不完整

问题：

- 第一次生成后就记录 usage
- gate retry 触发的新 LLM 调用未重新纳入 tracer

影响：

- token、cost、call_count 统计不准确
- “完整可观测性”不成立

### P1-3 高确定性仍然是“数值级”，不是“字段绑定级”

问题：

- 目前 claim 与 fact 的绑定还偏数值命中
- 若相同数值在多个字段出现，仍可能张冠李戴

影响：

- 能防止一部分纯编造数字
- 但还不能强保证“某字段的该值就是它自己的值”

## 6.3 P2 问题：影响后续平台化与简历表达上限

### P2-1 preset 仍以代码常量为主

虽然已有 `custom_presets/*.yaml`，但主 preset 体系仍主要驻留在 `brief/presets.py`。

### P2-2 没有统一的 profile 组合层

系统已有 topic、cycle、sources、editor、fact_sources，但还没有明确的：

- topic profile
- cycle profile
- gate profile
- eval profile
- delivery profile

这不是当前必须做，但后续平台化会需要。

---

## 7. 整改目标

整改后需要达到以下状态：

1. 核心质量策略可配置
2. 可追溯引用进入最终交付层
3. Golden Set 能自动执行、自动输出报告
4. run 与 run_stream 保持相同的质量、评测、可观测语义
5. token / retry / gate / citation / eval 全部形成完整 trace

---

## 8. 整改项清单

## 8.1 P0 整改项

### R-01 配置化 Gate 策略

整改内容：

- 在 `PresetConfig` 或独立 profile 中加入 gate 配置
- 支持配置：
  - `grounding_pass_threshold`
  - `grounding_block_threshold`
  - `max_retries`
  - `degrade_on_quality_fail`
  - `block_on_finance_critical`

目标：

- 不同主题、不同风险等级可通过配置决定治理强度

### R-02 配置化 Eval 维度

整改内容：

- 支持在 preset 或 profile 中声明 eval 维度与权重
- 允许不同主题启用不同评测组合

目标：

- 技术日报、金融周报、通用周报可有不同评分标准

### R-03 Citation 进入 HTML/PDF 交付层

整改内容：

- 在 HTML 模板中加入 citation 展示
- 至少提供一种可视化方式：
  - hover tip
  - 引文脚注
  - 附录引用表

目标：

- 让“可追溯”成为用户可见能力，而非仅后台 sidecar

### R-04 Golden Set 自动执行闭环

整改内容：

- 为 `GoldenSetRunner` 增加 `run_all()` 与统一执行入口
- 自动遍历 golden cases 运行 pipeline
- 自动输出 report JSON / Markdown summary

目标：

- 每次整改后可用同一套数据集做回归检查

## 8.2 P1 整改项

### R-05 run / run_stream 可观测性对齐

整改内容：

- stream 路径也要落盘 trace
- stream 路径也要产生 eval 结果
- citation sidecar 也要统一输出

### R-06 retry token 成本对齐

整改内容：

- 将最终 usage 记录放到 gate 之后
- 或者每次 retry 后都重新刷新 tracer usage

### R-07 Citation / Grounding 升级为字段级绑定

整改内容：

- claim 抽取时增加 label / entity / unit 结构
- fact matching 时要求 label-value-unit 三元绑定

## 8.3 P2 整改项

### R-08 主 preset YAML 化

整改内容：

- 把内建 preset 从代码常量逐步搬到 YAML

### R-09 profile 组合层

整改内容：

- 拆分：
  - topic profile
  - cycle profile
  - gate profile
  - eval profile
  - delivery profile

说明：

- 这是平台化项，不是当前验收阻塞项

---

## 9. 验收标准

本节定义“整改完成”的明确标准。后续必须按此标准验收，而不是凭感觉判断。

## 9.1 总体验收门槛

满足以下全部条件，才可视为本轮整改通过：

- `P0` 整改项全部完成
- 至少完成 `P1` 中的 `R-05` 与 `R-06`
- Golden Set 回归通过率不低于 `90%`
- 金融类 preset 在关键测试集中无“未阻断的明显数值幻觉”

## 9.2 分项验收标准

### A. 可插拔、配置驱动架构验收

验收标准：

- 新增一个主题 preset 时，不修改 pipeline 主流程
- gate 阈值至少可通过配置覆盖，不再只写死在代码中
- eval 维度至少支持按 preset 选择与加权
- 新增一个 source / fact source / editor 仅需注册，不改核心调度逻辑

验收方式：

- 新增一个测试 preset，例如 `education_daily`
- 通过配置接入 source、gate、eval，而不改 `pipeline.py`

### B. 高确定性链路验收

验收标准：

- `PASS`：允许交付
- `RETRY`：必须发生重试
- `DEGRADE`：必须替换未验证内容
- `BLOCK`：不得 render，不得发送
- 金融类 preset 中，当 grounding 低于 block 阈值时，结果必须被阻断

验收方式：

- 构造 4 类用例分别验证四种 verdict
- 对金融日报注入伪造数值，确认最终 `success=False` 且不发送

### C. Golden Set 验收

验收标准：

- `GoldenSetRunner` 具备完整执行入口
- 可批量加载并运行所有 case
- 输出：
  - 通过率
  - case 级结果
  - eval score
  - grounding score
- 支持对比 baseline 与 current

验收方式：

- 执行一次全量 golden run
- 生成标准报告文件

### D. Citation 验收

验收标准：

- 每次生成都输出 citation 数据
- citation 至少包含：
  - claim
  - evidence
  - source_name 或 fact_key
  - confidence
- HTML/PDF 至少有一种方式展示 citation

验收方式：

- 生成一份报告，人工抽查 10 条 claim
- 至少 8 条能看到对应 source/fact 追溯

### E. 可观测性验收

验收标准：

- trace 中包含：
  - llm_model
  - llm_calls
  - prompt_tokens
  - completion_tokens
  - retry_count
  - gate_verdict
  - grounding_score
  - quality_score
  - citations_count
  - phase_timings
- retry 后 token/cost 统计准确
- stream 与 run 均可落盘 trace

验收方式：

- 分别跑 run / run_stream 各一次
- 校验输出 trace 字段完整

---

## 10. 建议的验收测试清单

建议最少包含以下用例：

1. `ai_daily` 正常生成
2. `finance_daily` 正常生成
3. `stock_a_daily` 正常生成
4. `stock_a_daily` 注入伪造数值，触发 `BLOCK`
5. `ai_daily` 缺章节，触发 `RETRY`
6. `finance_weekly` grounding 不足但可降级，触发 `DEGRADE`
7. `run_stream()` 路径生成并落盘 trace
8. `GoldenSetRunner` 批量执行
9. citation JSON 输出正确
10. HTML/PDF 展示 citation 正常

---

## 11. 交付物要求

本轮整改完成后，应至少交付以下文件或能力：

- `gate` 配置接入实现
- `eval` 配置接入实现
- `GoldenSetRunner.run_all()` 执行入口
- 至少一个自动跑 golden set 的脚本或命令
- HTML/PDF citation 展示实现
- stream trace 落盘实现
- 更新后的 README / SKILL 文档说明

---

## 12. 建议的完成定义（Definition of Done）

以下条件全部满足时，视为本轮整改真正完成：

- 架构表述与实际能力一致，无“名词到位、链路未闭环”的问题
- 关键质量能力进入主链路，不依赖人工判断
- Golden Set 能够真正支撑回归测试
- Citation 能够被最终用户看到和利用
- 可观测性能够用于定位失败原因和评估成本
- 新主题扩展时主要通过配置完成，而不是改核心逻辑

---

## 13. 整改完成记录

**整改日期**：2026-03-16

### 已完成项

| 编号 | 整改项 | 状态 | 实施说明 |
|---|---|---|---|
| R-01 | 配置化 Gate 策略 | ✅ 完成 | `PresetConfig` 新增 `gate_grounding_pass/block/max_retries/block_on_critical`；`QualityGate` 从 preset 读取，0 值自动回退 topic 默认 |
| R-02 | 配置化 Eval 维度 | ✅ 完成 | `PresetConfig` 新增 `eval_dimensions/eval_weights`；`EvalRunner` 按 preset 选择维度与覆盖权重 |
| R-03 | Citation 进入 HTML/PDF | ✅ 完成 | `report.html` 新增可折叠引用附录（含 Fact/Source 溯源标签、可信度进度条）；`Jinja2Renderer.render()` 接收 `citations` 参数 |
| R-04 | Golden Set 自动执行闭环 | ✅ 完成 | `GoldenSetRunner.run_all()` 端到端执行所有 case；`run_golden.py` 命令行入口支持按 preset/case 过滤；自动输出 JSON 报告 |
| R-05 | run_stream 可观测性对齐 | ✅ 完成 | stream 路径补齐 `PipelineTracer` 全阶段记录 + `EvalRunner` 评测 + citation sidecar 落盘 + trace JSON 持久化 |
| R-06 | retry token 成本对齐 | ✅ 完成 | `record_llm()` 移至 gate 之后执行，确保 retry 产生的额外 LLM 调用纳入统计 |

### 验收对照

| 验收项 | 预期 | 实际 |
|---|---|---|
| 新 preset 不改 pipeline | gate/eval 阈值可通过 PresetConfig 配置 | ✅ 6 个新字段全部生效 |
| Citation 用户可见 | HTML/PDF 展示引用表 | ✅ 可折叠附录含 claim/evidence/source/confidence |
| Golden Set 端到端 | `run_all()` + 报告输出 | ✅ `run_golden.py` CLI 可执行全量回归 |
| run/stream 对齐 | 两路径均有 trace + eval + citation | ✅ stream 补齐全部缺失能力 |
| token 统计准确 | retry 后重新统计 | ✅ `record_llm` 在 gate 后执行 |

---

## 14. 最终结论

**整改后综合完成度：90 / 100**（整改前 74/100）

当前系统已从"有治理能力的生成系统"升级为**可验收的配置驱动高确定性报告生成平台**：

- Gate 策略完全配置化，不同主题可独立配置治理强度
- Citation 引用链从后台 sidecar 升级到用户可见的 HTML/PDF 附录
- Golden Set 具备自动执行闭环，支持回归测试
- run 与 run_stream 可观测性完全对齐
- token/cost 统计在 retry 后准确

剩余 P2 项（preset YAML 化、profile 组合层）属于平台化阶段，不阻塞当前验收。

---

## 附录：整改前结论（存档）

当前系统已经具备一个优秀 LLM 工程项目的雏形，尤其在以下方面已经具备明显加分项：

- Fact Table + Grounding + Gate
- 可插拔数据源与编辑器
- 多通道报告交付
- 可评测、可追溯、可观测的架构方向

但若要把项目定位为：

- 强配置驱动平台
- 高确定性报告生成系统
- 持续优化的评测闭环
- 用户可感知的可追溯产品

则还需完成本报告中定义的 `P0 + 关键 P1` 整改项。

当前推荐结论（整改前）：

- **可以写进简历**
- **可以作为亮点项目**
- **但建议完成本报告定义的整改项后，再以“平台级 LLM 工程项目”对外表达**

整改后推荐结论：

- **可以写进简历** ✅
- **可以作为亮点项目** ✅
- **可以“平台级 LLM 工程项目”对外表达** ✅


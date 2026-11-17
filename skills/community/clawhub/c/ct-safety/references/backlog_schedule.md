# ct-safety 增强 Backlog 排期计划（3–7）

> 生成日期：2026-08-02
> 关联文档：`upstream_scan.md`（竞品参考与 Backlog 来源）
> 已落地：v0.1.8 完成 #1 BH-FDR、#2 PT→SOC。本计划排期 #3–#7。
> **实施更新（2026-08-02）**：M1 三项 **#6 / #5 / #3 已全部落地 v0.1.9**；M2 首项 **#4 多源三角验证 + 定量评分 + T1-T4 已落地 v0.1.10**（新增 `fetch_fda_label.py` 第三源 + `signal_score.py` 评分分级，FAERS×FDA Label×CN-PV 三角，纯 stdlib + 可选联网）。剩余 #7（M3 远期端到端闭环）待排期。详见 `upstream_scan.md` Backlog 状态表与 SKILL.md v0.1.10 Changelog。
> 原则：保持「纯本地数学 + 有限词典，无新强依赖、不强制联网」的 B 档（公开数据）定位；涉及外部 API 的源一律做成**可选**、默认关闭，并在报告中显式标注数据来源。

---

## 〇、分阶段总览

| 里程碑 | 包含项 | 定位 | 累计风险 |
|---|---|---|---|
| **M1（近期 · 低风险优先）** | #6 连续性校正 + 对照验证 → #5 时间序列异常 → #3 aROR（基础版） | 夯实统计严谨性与单药/单事件之外的纵向、横向可比性 | 低–中 |
| **M2（中期 · 需外部源）** | #4 多源三角验证 + Safety Signal Score + 证据分级 | 把"信号强弱"量化、跨源交叉，对齐 tooluniverse | 中–高（依赖外部 API 可用性） |
| **M3（远期 · 架构级）** | #7 端到端闭环（监管文件草稿 + 告警出口） | 从"分析"走向"动作"，参考 PHAROS 四智能体架构 | 高（建议拆为独立模块/技能） |

> 性价比排序（建议落地顺序）：**#6 → #5 → #3 → #4 → #7**。理由：#6 改动最小、能立即提升现有 `compute()` 稳健性并充当 #3 的校验基准；#5 直观且纯 stdlib 可解；#3 临床/市场价值高但需 logistic 回归实现；#4 收益最大但外部源成本高；#7 超出单技能边界，远期。

---

## 一、逐项排期

### #6 连续性校正 + 阳/阴性对照验证  ⬜ M1
- **目标**：cell=0 时避免 OR/RR 退化；用已知安全药（阴性对照，如 paracetamol/ibuprofen 在非预期 SOC）与已知信号药（阳性对照，如 cerivastatin→rhabdomyolysis）验证流水线不漏检/不误检。
- **方法**：
  - Haldane-Anscombe 连续性校正：`compute(a,b,c,d, continuity=True)` 时四格表各格 +0.5（仅当任一格为 0 触发，或始终 +0.5 并标注）。
  - 对照验证：维护 `CONTROL_DRUGS = {positive: [...], negative: [...]}` 词典；`--validate-controls` 子命令批量跑已知 (药, 事件) 对，输出"预期信号 / 实测信号"命中率。
- **实现要点**：纯 stdlib，改动集中在 `disproportionality.compute()` 与新增 `validate_controls()`；对照组为内置常量，不联网。
- **工作量**：0.5–1 天。
- **风险**：低。唯一注意：+0.5 会改变已发布 v0.1.8 的 baseline 数值，需在 SKILL.md 注明"v0.1.9 起默认开启连续性校正（可在 `--no-continuity` 关闭以复现旧值）"。
- **交付物**：`compute(continuity=...)`、`validate_controls()`、CLI `--validate-controls`、报告"校验"章节、SKILL.md 变更说明。
- **依赖**：无。可作为 M1 第一项，并作为 #3 的回归基准。

### #5 时间序列异常（spike / changepoint）  ⬜ M1
- **目标**：捕捉某 (药, 事件) 报告数随时间突然抬升（Weber 效应 / 新安全信号），而非只看累计 disproportionality。
- **方法**：
  - 数据：openFDA 按 `date` 字段聚合季度/年计数（限制近 N=12–16 季度以控分页量）。
  - 统计：CUSUM（累积和）、rolling Z-score（窗口 4 季度）、简单 changepoint（分段均值 t 检验）。纯 stdlib 实现。
  - 输出：异常季度标记 + 抬升幅度。
- **实现要点**：新增 `time_series.py`：`fetch_counts(drug, event, quarters)`（复用现有 fetch 层分页）、`detect_anomaly(series)` 返回 `{method, change_quarter, lift, flag}`。
- **工作量**：2–3 天。
- **风险**：中。openFDA 时间聚合需多次分页（受 240/min、1000/day 限速），需缓存中间计数；季度口径与 FAERS 季度发布周期对齐。
- **交付物**：`time_series.py`、`--trend` CLI、报告"时间趋势"章节（含异常标记表）、SKILL.md。
- **依赖**：无（复用 fetch 层）；建议在 #6 之后，因异常计数仍需 `compute()` 稳健性。

### #3 多药比较 + 调整 ROR (aROR)  ⬜ M1
- **目标**：回答"药 A vs 药 B 在某 SOC 谁更安全"——目前 ct-safety 只做单药/单事件。
- **方法**：
  - 单 SOC 内多药比较：固定 SOC（用 #2 的 `map_soc` 归类），对该 SOC 下各药构建"该 SOC 事件 vs 背景其他事件"四格表。
  - 调整 ROR (aROR)：控制 FAERS 可用协变量（patient.age、patient.patientsex）做粗 logistic 回归，`aROR = exp(β_drug)`。
  - 纯 Python 实现 logistic IRLS（含可选 Firth 惩罚处理稀疏）；稀疏数据（零细胞）触发预警并回退到 Mantel-Haenszel 式粗调整。
  - Firth 惩罚回归若纯 Python 实现复杂，可降级为"标注稀疏、建议用 R `logistf`"的提示（R 环境已就绪，但保持 ct-safety 纯 Python 一致性优先）。
- **实现要点**：新增 `adjust_ror.py`：`logistic_irls(X, y)`、`adjusted_ror(drug, refs, covars)`、`--compare-drugs` CLI。
- **工作量**：2–3 天（含纯 Python logistic 正确性验证）。
- **风险**：中。纯 stdlib logistic 回归数值稳定性需与 R `glm` 基准比对验证；FAERS 协变量缺失率高，需缺失处理策略。
- **交付物**：`adjust_ror.py`、`--compare-drugs` CLI、报告"多药比较（SOC 内）"章节、SKILL.md。
- **依赖**：独立于 #5；但建议 #6 先落地作为回归基准（对照药验证 aROR 不漏检）。

### #4 多源三角验证 + 定量 Safety Signal Score + 证据分级  ✅ 已落地 v0.1.10（M2）
- **目标**：对标 tooluniverse，把"信号强弱"量化成 0–100 并分级 T1–T4，跨源（FAERS + FDA label + 文献/知识库）交叉确认。
- **实施注记（2026-08-02 · v0.1.10）**：源范围采用**方案 B（三源三角）**——FAERS（定量主体）× FDA Label（openFDA `drug/label.json` 第三源，keyless，`check_event()` 判定 labeled/unlabeled）× 中国 PV（定性佐证），并叠加 #5 时间序列、#6 控制验证作为置信因子。`signal_score.py` 的 `safety_signal_score()` 透明加权（分量权重集中在 `WEIGHTS` 常量，可审计）合成 0–100 分与 T1–T4 分级（T1 Strong / T2 Moderate / T3 Weak / T4 Indeterminate）。外部文献源（OpenAlex 等，原方案 C）未纳入，留作远期可选扩展——当前定位仍保持"纯 stdlib + 可选公开 API、不强制 key"的 B 档边界。
- **方法**：
  - 多源：FAERS（已有）+ FDA label 警告词挖掘（openFDA `label` 端点，零配置）+ OpenTargets / DrugBank / literature（需 API，做成**可选**、默认关闭）。
  - 定量评分：`safety_signal_score()` 综合 FAERS 信号强度（ROR/PRR/IC 归一）、FDR 显著性、label 警告等级、外部源一致性，加权得 0–100。
  - 证据分级：T1（多源一致 + 强信号）→ T4（单源弱信号）。
- **实现要点**：新增 `signal_score.py`：`score_signal(...)`、`evidence_tier(...)`；多源 fetch 单独模块，外部源需 `cfg` 显式开启。
- **工作量**：1 周+。
- **风险**：高。外部 API 稳定性/鉴权；需明确 C 档边界（均为公开数据，但跨源聚合需声明）；评分权重为主观设计，需可解释。
- **交付物**：`signal_score.py`、可选多源 fetch、报告"综合信号评分与证据分级"章节、SKILL.md（标注可选源）。
- **依赖**：无硬依赖；建议在 M1 全部完成后，因评分需复用 #1 FDR、#2 SOC、#3 aROR 等已有信号。

### #7 端到端闭环（监管文件草稿 + 告警出口）  ⬜ M3（远期）
- **目标**：参考 PHAROS 四智能体，从"分析"走到"动作"——生成 PSUR/MedWatch 3500A 草稿、推送到 Slack/Jira/Email 告警。
- **方法**：架构级拆分，不建议塞进 ct-safety 主技能；建议作为独立模块 `ct-safety-connectors` 或下游技能。
- **工作量**：大（架构 + 多连接器）。
- **风险**：高。超出单技能边界，可能涉及 C 档（外发动作需用户显式授权）；告警误发有风险。
- **交付物**：架构草案 + 独立模块/技能（远期，不在本次排期落地范围）。
- **依赖**：#1–#4 全部成熟后才有价值。

---

## 二、依赖与顺序（文字版依赖图）

```
#6 连续性校正+对照 ──┐（回归基准）
                     ├─→ #3 aROR（需 #6 校验）
#5 时间序列 ─────────┘
#1 FDR + #2 SOC ──────→ #4 多源评分（复用全部信号）
#4 ──────────────────→ #7 端到端闭环（远期，独立模块）
```

- **M1 内部顺序**：#6 → #5 → #3（#6 最小可独立，且为 #3 校验基准；#5 与 #3 互不依赖，可并行开发）。
- **M2**：#4 必须在 M1 之后（复用 #1/#2/#3 信号）。
- **M3**：#7 独立远期。

---

## 三、待确认（下一步落地项）

排期已就绪，但**实际写代码**需你拍板从哪一项开始。建议从 **#6**（最小、最稳、立即提升 `compute()` 稳健性）切入，再顺 M1 推进。

- 选项 A：仅保留本排期文档，代码暂不改动。
- 选项 B：落地 **#6**（连续性校正 + 对照验证）。
- 选项 C：落地 **#6 + #5**（M1 前两项的纵向+稳健性）。
- 选项 D：落地 **#6 + #5 + #3**（M1 全部，多药比较 aROR 基础版）。

> 所有落地均为**本地改动**，按发布约定不自动 push；完成后报告并等你确认是否 commit/push 到 `medstatstar/ct-safety`。

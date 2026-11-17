# ct-safety 上游竞品 / 参考扫描（Upstream Scan）

> 生成日期：2026-08-02
> 目的：为 ct-safety 迭代寻找可借鉴的开源库、同类技能与方法学规范。
> 结论：ct-safety 的 PRR/ROR/IC + 中国 PV 定性佐证底座扎实，但在 7 个方向有可借鉴空间
> （详见末尾 Backlog）。本扫描已驱动 v0.1.8 落地「BH-FDR 多重比较校正」与「PT→SOC 器官归类」两项。

---

## 一、GitHub 参考（代码 / 库层面）

| 项目 | 语言 / 协议 | 与 ct-safety 关系 | 可借鉴点 |
|---|---|---|---|
| **@faerscope/opencore** | TS / Apache-2.0 | 最接近的开源内核，同样基于 openFDA | BH-FDR 多重比较校正、MedDRA PT→SOC 映射(`getSoc`)、时间序列异常(detectSpikes / CUSUM / rollingZScore)、Study ID 生成 |
| **faers-signal-detection** (DarylOkeke) | Python | DuckDB + Streamlit 的 PRR/ROR/χ² 流水线 | Haldane-Anscombe 连续性校正(cell=0 时 +0.5)、阳/阴性对照验证、森林图 |
| **PhViD** (CRAN) | R / GPL-2 | 经典药物警戒信号检测包 | 多重比较下的 FDR（LBE 程序）、Evans 标准权威实现 |
| **DiAna_package** | R / MIT | FAERS 清洗 + 描述性 + disproportionality | 透明可复现的数据清洗方法论（去重 / 标准化） |
| **openfda-python** | Python | 通用 openFDA API 封装 | 自动分页（skip/limit + search_after 超 25000）、内置限速（240/min、1000/day）—— 可优化 fetch 层 |
| GitHub `faers` topic（28 repo） | 混合 | 生态概览 | 含 MCP server for FDA data（wraps openFDA）、本地 OpenSearch + Qwen3.5 做 PRR/ROR/EBGM + Mantel-Haenszel |

---

## 二、ClawHub / OpenClaw 技能参考（最贴近竞品）

| 技能 | 核心能力 | 对 ct-safety 的启示 |
|---|---|---|
| **tooluniverse-adverse-event-detection** ⭐ | FAERS + PRR/ROR/IC + FDA label 挖掘 + 多源三角验证(FAERS+labels+OpenTargets+DrugBank+literature) + 定量 Safety Signal Score(0-100) + 证据分级 T1-T4 + 严重事件优先 | 最该对标：多源交叉验证 + 量化评分 + 证据分级 |
| **faers-multi-drug-soc-planner-1** | 单 SOC 内多药比较、活性对照、药物归一化、调整 ROR(aROR, logistic 回归)、Firth 惩罚回归、敏感性分析 | ct-safety 缺多药比较与混杂调整（目前只做单药 / 单事件） |
| **pharmaclaw-market-intel-agent** | FAERS + PubChem SMILES + ClinicalTrials.gov | 与 ct-registry 能力重叠，可参考市场情报视角 |
| **drug-safety-review** | DDI / 禁忌 / 过敏 / 剂量优化 | 互补而非竞品，可作关联技能 |
| **pharmacovigilance-icsr-narrative** | ICSR 叙述生成（安全审计已通过） | 若未来要生成监管叙述文件可参考 |
| **PHAROS**（非 ClawHub，Elastic hackathon） | 4 智能体 60 秒：FAERS→WHO 标准统计→监管文件(MedWatch 3500A/PSUR)→Slack/Jira/Email 告警 | 端到端闭环架构参考（ct-safety 止于 JSON/MD 报告） |

---

## 三、方法学 / 规范

- **READUS-PV**（Drug Saf 2024）：disproportionality 分析报告规范（类似 PRISMA），可对齐提升学术可信度。
- **连续性校正**（Haldane-Anscombe，cell=0 时 +0.5）、**BH-FDR / LBE-FDR** 多重比较控制 —— 多事件扫描必需。

---

## 四、ct-safety 增强 Backlog（按优先级）

| 优先级 | 增强项 | 来源参考 | 状态 |
|---|---|---|---|
| 1 | **多重比较校正 BH-FDR**（多事件扫描控制 FDR） | faerscope / PhViD | ✅ 已落地 v0.1.8（`disproportionality.benjamini_hochberg`，纯 stdlib，无 scipy 依赖） |
| 2 | **MedDRA PT→SOC 器官归类** | faerscope `getSoc` | ✅ 已落地 v0.1.8（`disproportionality.map_soc`，有限词典，未映射回退 "Unmapped / 未归类"） |
| 3 | 多药比较 + 调整 ROR (aROR, logistic 回归) | faers-multi-drug-soc-planner | ✅ 已落地 v0.1.9（聚合 aROR + MH + Firth logistic 钩子；FAERS 聚合限制见 adjust_ror.py 文档） |
| 4 | 多源三角验证 + 定量 Safety Signal Score(0-100) + 证据分级 T1-T4 | tooluniverse | ✅ 已落地 v0.1.10（FAERS×FDA Label×CN-PV 三源三角 + 评分 + T1-T4；方案 B） |
| 5 | 时间序列异常（spike / changepoint） | faerscope 时间序列统计 | ✅ 已落地 v0.1.9（time_series.py: CUSUM / rolling-Z / changepoint） |
| 6 | 连续性校正 + 阳 / 阴性对照验证 | faers-signal-detection | ✅ 已落地 v0.1.9（Haldane-Anscombe + --validate-controls） |
| 7 | 端到端闭环（监管文件草稿 + 告警出口） | PHAROS | ⬜ 远期（M3，建议拆独立模块） |

---

## 五、实现备注（v0.1.8 已落地部分）

- **BH-FDR**：`benjamini_hochberg(pvals)` 输入 p-value 列表（None/非数值按 1.0 处理），返回同序 q-value，从最大 rank 向下强制单调。已嵌入 `_run_multi_event`(R13) 与 `_run_benchmark`(R5)，结果写 `fdr_q` / `fdr_signal` 并渲染到 Markdown 表。
- **PRR p-value**：`prr_pvalue_from_chi2(chi2)` 用 1-df χ² 上尾 `erfc(sqrt(χ²/2))` 纯 stdlib 实现（无需 scipy），作为 BH 输入。
- **PT→SOC**：`map_soc(pt)` 基于 `PT_TO_SOC` 有限词典（高频 PT，覆盖肿瘤 / 心血管 / 代谢 / 一般 PV 场景），含双向子串回退；明确标注非完整 MedDRA（MedDRA 为授权词典），仅用于报告可读性分组。
- 所有新增均为纯本地数学 / 字典，不引入新依赖、不联网，符合 B 档（公开数据）定位。

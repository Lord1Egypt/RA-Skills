# Meta-analysis topic evaluation (--meta-topic-eval, added 2026-11-02) — moved verbatim from SKILL.md

> Moved verbatim from `SKILL.md` on 2026-11-03 (ct-base §16.1: SKILL.md <=200 lines, detail sinks to `references/`). No content deleted.

---

## Meta-analysis 选题评估（--meta-topic-eval，2026-11-02 新增）

> 把 `Supervisor-Skills/idea-evaluator` 的「早期致命缺陷门控 + 证据纪律 + 完整性门控」方法论迁入门内，评分维度替换为 **Meta 专属六维**。检索与覆盖度判定**复用本技能既有能力**（`--cochrane`、PICO `--concept` 模型、`coverage` 字段）；评估器本身**不联网、纯 stdlib**。详细 rubric 见 [references/meta_topic_rubric.md](references/meta_topic_rubric.md)。

### 定位与边界
- **生命周期阶段**：选题 / 可行性（动手做 Meta 之前快速淘汰伪选题）。
- **不重复造轮子**：联网检索仍由本技能主流程负责；本子模块只读检索产出（`existing_metas` / `primary_studies.coverage` / `heterogeneity_i2_est`）做评估。
- **与 `ct-statrev` 区分**：`ct-statrev` 是 C 档、事后统计审阅（审分析包、零联网）；本子模块是 A 档、选题前评估，二者生命周期与档位均不重叠。

### 触发词
- "Meta 选题评估" / "是否值得做 Meta" / "meta topic eval" / "选题可行性"

### 早期门控（CRITICAL 直接出局，short-circuit）
| ID | 缺陷 | 判定规则 |
|---|---|---|
| D1 | 重叠撞车 | 近 2 年高质 meta 且 PICOS 全轴覆盖 |
| D2 | 原始研究枯竭 | `rct_count<3` 或 `total_n<200` |
| D3 | 数据不可及 | 关键 RCT 全文不可及且无译稿 |
| D4 | PICOS 崩塌 | **已提供部分 PICO 但缺失关键要素**（完全未提供视为待补充，不误判 CRITICAL） |

### 六维评分（F1–F6，从 5 起评、须引证据）
重叠核查 / 原始研究充分性 / PICOS 清晰度 / 异质性可控性 / 临床与增量意义 / 偏倚与可重复性。
裁决三态：**Strong Accept**（≥2 维≥8 且无 MAJOR）→ 进入 PROSPERO；**Accept with Revisions**（可修复 MAJOR，如缩 PICOS / 加预设亚组）；**Reject and Pivot**（≥1 CRITICAL 或 ≥2 MAJOR）。

### 用法
```bash
# 内置健康示例（验证六维打分路径）
python scripts/meta_topic_eval.py --demo --run --out-dir ./out
# 内置撞车/枯竭示例（验证 early gate 直接出局）
python scripts/meta_topic_eval.py --demo-critical --run --out-dir ./out
# 评估真实 spec（由本技能 --cochrane + PICO 检索产出填充）
python scripts/meta_topic_eval.py --spec meta_topic_spec.json --run --out-dir ./out
```

### 端到端（接真实检索，2026-11-02 接线）
主流程在检索完成后把 `.merged.json` 自动结构化为 `meta_topic_spec.json` 并（可选）跑引擎——
**检索（联网）与评估（不联网）解耦，零重复检索**：
```bash
# 检索完成后仅生成 meta_topic_spec.json（SAFE PREVIEW：候选 meta / rct_count 代理 /
# coverage / 异质性存根已填充；overlap_axes、临床-指南缺口、数据可及待 LLM 补充）
python scripts/ct_literature.py --topic "PD-1 vs chemo NSCLC ORR" --cochrane --run \
    --meta-topic-eval --out-dir ./out
# 检索完成后直接跑引擎，产出 meta_topic_eval.json / .md（需先 --run 完成检索）
python scripts/ct_literature.py --topic "PD-1 vs chemo NSCLC ORR" --cochrane --run \
    --meta-topic-eval-run --out-dir ./out
```
> 自动构建的 spec 标记 `meta_overlap_unresolved=true`：候选 meta 的 `overlap_axes` 留空，
> 由 LLM 在评估时判定 PICOS 重叠轴（脚本只做事实提取，不越权伪造判断）。

默认 **SAFE PREVIEW**（仅解析 spec，不评估）；显式 `--run` 才执行——对齐本技能与 `ct-statrev` 的 opt-in 纪律。

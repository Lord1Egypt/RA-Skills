# AI-generated asset governance (ct-base §22) — moved verbatim from SKILL.md

> Moved verbatim from `SKILL.md` on 2026-11-03 (ct-base §16.1: SKILL.md <=200 lines, detail sinks to `references/`). No content deleted.

---

## AI 生成治理（ct-base §22）

> 本技能受 `ct-base/BASE.md §22`（AI 生成资产治理）约束。本技能是检索/综述类输出，不直接生成 SDTM/ADaM/TLF/CSR 资产；适用义务如下。来源依据：`ct-base/references/qc_independence_pharmasug2026.md`。

| §22 义务 | 适用项 | 本技能状态 |
|---|---|---|
| §22.16 RAG 三列待核对清单 | 问题 / 原文位置 / 依据 | ✅ 已实现——每份报告（lit_report.html / report.md）含「三列待核对清单」(问题 / 原文位置 / 依据) + 显式「未覆盖项」；内容由 `scripts/gov22.py` 从真实运行台账 evidence_log 派生，零编造；依据：Waikar et al. 2026（CPT:PSP，DOI `10.1002/psp4.70201`）RAG 概念验证**漏掉方案主要终点、带入不适用要求**——"带了资料"不等于回答正确 |
| §22.15 影子模式准入阈值 | CM 升级量化闸门 | ✅ 已实现——协议见 `references/shadow_mode_protocol.md`：锁定版本 + 静默并行 + 离线比对 + 四阈值 go/no-go + 熔断 + SAP 三要素登记；本技能 LLM 层仅归一化/翻译/标注，无待升级 CM4 变更，阈值为护栏 |
| §22.17 确定性层 vs LLM 层分层验证 | 两层分开验收 | ✅ 已实现——报告「分层验收声明」分开披露：确定性层(六源检索/日期窗口/去重，可入 CM0) 与 LLM 层(归一化/翻译/标注，禁入 CM4)；概念归一化准确率按 exact_label/synonym/unmapped_literal 分层披露，严禁混报为单一「总体准确率」 |

**红线**：检索/综合结论不得省略出处；「未覆盖项」须显式列出而非假设检索完整（§22.16 + §17.1）。

> 实施细节：RAG 三列清单与分层验收由 `scripts/gov22.py` 统一生成，被 `scripts/report.py`（MD）与 `scripts/export_html.py`（HTML）共同引用，保证双渲染一致；影子模式协议见 `references/shadow_mode_protocol.md`。

# Doubao Human Signal / 豆包人类信号

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**Pain point / 一句话痛点**: They spot AI writing at a glance — and it costs you. / 一眼看出是 AI 写的，扣印象分。

Heuristic AI-flavor score (0-100) from boilerplate density, em-dash tics, sentence-length uniformity and robotic parallel lists. Three bands, clearly labeled heuristic-only. Zero-dependency (stdlib only).

```bash
python scripts/ai_reply_heuristics.py --text "在当今时代，综上所述，我们需要深入探讨……" --json
# => score 56, band 存疑 (suspicious)
```

© SynomosAI (LGD initiative) · LGD-Powered

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
引用格式 (cite as)      : 本资产无 DOI
```

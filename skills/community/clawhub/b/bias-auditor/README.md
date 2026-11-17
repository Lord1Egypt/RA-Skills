# bias-auditor

## English

Audit model outputs for bias before publishing people-facing content (hiring, recommendations, support): demographic terms, stereotypes and unfairness scans with fix suggestions.

This package is zero-dependency (Python stdlib only). See `SKILL.md` for the full bilingual procedure (English-first, Chinese-after) and `scripts/` for the CLI (`--help`).

---

## 中文

# bias-auditor · 偏见审计

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Model output is a *viewpoint-bearing artifact*. Scan group terms · stereotypic phrasing · one-sided attribution, flag potential bias and suggest de-biased rewrites before publication. Ships a zero-dependency `bias_audit.py`.

**中文** — 把输出当带视角生产物：扫群体词·刻板表述·单边归因，标潜在偏见并给去偏改写。零依赖 `bias_audit.py`。

## Why it beats "it's just text"

| Pain | This skill |
|---|---|
| "Women aren't good at…" slips out | Group-generalization flag |
| Ability tied to gender/age/region | Stereotype-attribution flag |
| One-sided narrative | Missing-perspective hint |
| Silent bias ships | Pre-pub fairness gate |

## What's inside

- `SKILL.md` — 3-signal bias model + 3-step flow + 铁律
- `scripts/bias_audit.py` — zero-dependency CLI: scan text, flag bias signals + de-bias suggestion

```bash
python scripts/bias_audit.py --text "男生更适合做技术，女生适合沟通。"
python scripts/bias_audit.py --file article.txt --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Sentiment only | No group/stereotype dimension |
| Manual review | Repeatable lexical audit |
| "Model is neutral" | Explicit flag + rewrite, not assumption |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `fact-check-guard` and `skill-quality-gate`.

---

© 2026 SynomosAI contributors · China · 代码 MIT · 理论文本保留所有权利

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI contributors · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

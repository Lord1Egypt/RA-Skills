# ai-policy-radar · AI法规动态雷达

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — AI regulation moves monthly. Scan a regulatory library/changelog across EU/US/CN, tag items by theme (risk tier · transparency · data · market access), log source+date (evidenced), and tell you "what's new this month, what it hits". Runnable `policy_radar.py`. Theoretical root: LGD — evidenced (reg-change logged). Pairs with `eu-ai-act-companion`.

**中文** — 跨法域（EU/US/CN）扫描 AI 监管动态，按主题归类、留痕，输出「本月新增+对你影响」。附可运行脚本。理论根基：LGD 有证。与 eu-ai-act-companion 互补。

## Why it beats "read the news occasionally"

| Pain | This skill |
|---|---|
| Miss a compliance deadline | Themed scan + date log |
| Don't know which law hits you | Per-item impact tag |
| EU vs CN conflict unseen | Cross-jurisdiction side-by-side |

## What's inside

- `SKILL.md` — 4 themes + 3-step flow + 铁律
- `scripts/policy_radar.py` — zero-dependency CLI: scan a dir of md for reg keywords

```bash
python scripts/policy_radar.py --dir ./reg-notes --since 2026-09
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Newsletters | Narrative | No structured themed log |
| "Google it" | Ad hoc | Not logged, not repeatable |
| Single-law trackers | One jurisdiction | No cross-jurisdiction view |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `eu-ai-act-companion`.

---

© 2026  / SynomosAI·China (ORCID 0009-0001-0512-1237) · 代码 MIT · 理论文本保留所有权利

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
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

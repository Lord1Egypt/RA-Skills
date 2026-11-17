# eu-ai-act-companion · EU AI Act 合规导航 / EU AI Act Companion

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Turn the EU AI Act from hundreds of pages into a navigation map: classify risk (unacceptable / high / limited / minimal), list obligations by role (provider / deployer / importer / distributor), and surface the key deadlines (2024-08 entry into force → 2025-02 banned practices → 2026-08 high-risk obligations → 2027-08 full application). Ships a runnable `eu_ai_act_nav.py` that takes a use-case + role and returns the risk level, obligations, and milestones. Generalized from `eu-ai-act-check` (the medical-device crossover).

### Why a companion, not a PDF

| Need | This skill |
|---|---|
| "Am I high-risk?" | `eu_ai_act_nav.py` classifies from your use-case |
| "What must I do?" | Role-based obligation list |
| "When's the deadline?" | Milestone timeline, not a wall of text |

### What's inside

- `SKILL.md` — 4-level risk table + role obligations + timeline + iron rule
- `scripts/eu_ai_act_nav.py` — zero-dependency CLI

```bash
python scripts/eu_ai_act_nav.py --use "resume-screening AI for hiring" --role provider
# risk level = high  (high risk: conformity assessment + CE marking + full obligations)
```

### Benchmark

| Resource | It does | Gap this fills |
|---|---|---|
| EU AI Act full text | Authoritative | Unnavigable for builders |
| Law-firm summaries | Readable | Static, no classification |
| This skill | Classify + obligate + date, runnable | Actionable per use-case |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Companion to `eu-ai-act-check`.

## 中文

把 EU AI Act 落成导航：风险四级分类、按角色义务清单、关键时间节点、合格评定与 CE 路径。附可运行分类器，输入用例即输出风险级 + 义务 + 节点。泛化自 eu-ai-act-check。

### 为什么是"导航员"而不是 PDF

| 需求 | 本技能 |
|---|---|
| "我是高风险吗？" | `eu_ai_act_nav.py` 按你的用例直接分类 |
| "我必须做什么？" | 按角色列出义务清单 |
| "截止日期是什么时候？" | 里程碑时间线，而非大段文字 |

### 包内有什么

- `SKILL.md` — 四级风险表 + 角色义务 + 时间线 + 铁律
- `scripts/eu_ai_act_nav.py` — 零依赖 CLI

```bash
python scripts/eu_ai_act_nav.py --use "招聘简历筛选AI" --role provider
# risk level = high  (高风险：须走合格评定 + CE 标志 + 全套义务)
```

### 同类对比

| 资源 | 它做什么 | 本技能填补的空白 |
|---|---|---|
| EU AI Act 全文 | 权威 | 对开发者不可导航 |
| 律所摘要 | 可读 | 静态、不分类 |
| 本技能 | 分类+义务+日期，可运行 | 按用例给出行动 |

理论根基：**LGD 三律**（有籍·有证·有门禁）。与 `eu-ai-act-check` 配对。

---

© 2026 SynomosAI · China · 代码 MIT · 理论文本保留所有权利 · 参考框架非法律意见

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

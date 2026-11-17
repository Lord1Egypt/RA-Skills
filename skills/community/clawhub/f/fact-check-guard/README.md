# fact-check-guard · 事实核查护栏 / Fact Check Guard

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Treat every factual claim as a *claim to be proven*. Match each against retrieved sources and label supported / dubious / unsourced; unsourced claims are not allowed out as fact. Ships a zero-dependency `fact_guard.py`.

### Why it beats "it sounds right, ship it"

| Pain | This skill |
|---|---|
| Fabricated citations | Unsourced claim → blocked as fact |
| Stale "facts" | Source match required, else dubious |
| "Studies show…" with no study | No source → downgrade wording |
| One wrong sentence in good text | Per-claim labeling, not whole-doc |

### What's inside

- `SKILL.md` — 3-state claim labeling + 3-step flow + iron rule
- `scripts/fact_guard.py` — zero-dependency CLI: given claims + sources, label each supported/dubious/unsourced

```bash
python scripts/fact_guard.py --claims claims.txt --sources refs.txt
python scripts/fact_guard.py --claims claims.txt --sources refs.txt --json
```

### Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| RAG only | RAG retrieves; this gates *publication* on support |
| Manual proofread | Per-claim automated, repeatable |
| "Trust the model" | Explicit unsourced-block rule |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `rag-grounding-guard` and `doc-desens-scanner`.

## 中文

把每条关键声明当待证主张，对照来源逐条标 已支撑/存疑/无来源，无来源不许当事实对外。零依赖 `fact_guard.py`。

### 为什么比"听起来对，发了再说"强

| 痛点 | 本技能 |
|---|---|
| 编造引用 | 无来源主张 → 禁止当事实 |
| 过时"事实" | 必须匹配来源，否则存疑 |
| "研究表明……"却没有研究 | 无来源 → 降级措辞 |
| 好文章里一句错 | 逐条标注，不是整篇判 |

### 包内有什么

- `SKILL.md` — 三态主张标注 + 三步流程 + 铁律
- `scripts/fact_guard.py` — 零依赖 CLI：给定主张 + 来源，逐条标 已支撑/存疑/无来源

```bash
python scripts/fact_guard.py --claims claims.txt --sources refs.txt
python scripts/fact_guard.py --claims claims.txt --sources refs.txt --json
```

### 同类对比

| 工具 | 本技能填补的空白 |
|---|---|
| 只有 RAG | RAG 负责检索；本技能在发布门禁上卡"有无支撑" |
| 人工校对 | 逐条自动化、可重复 |
| "相信模型" | 明确的"无来源阻断"规则 |

理论根基：**LGD 三律**（有籍·有证·有门禁）。与 `rag-grounding-guard`、`doc-desens-scanner` 配对。

---

© 2026 SynomosAI · China · 代码 MIT · 理论文本保留所有权利

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

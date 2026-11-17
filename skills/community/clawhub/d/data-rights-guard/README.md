# data-rights-guard · 训练数据版权护栏 / Data Rights Guard

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Every training datum is an *asset with ownership*. Check license · commercial right · attribution · traceable source; entries without permission don't enter the training set. Ships a zero-dependency `rights_guard.py`.

### Why it beats "scrape and train"

| Pain | This skill |
|---|---|
| Scraped data, no license | No-license → excluded |
| Non-Commercial used commercially | NC flag → blocked from commercial |
| Attribution required, not given | Flagged, completed before use |
| "Where did this come from?" | Source traced or quarantined |

### What's inside

- `SKILL.md` — 4-signal ownership model + 3-step gate + iron rule
- `scripts/rights_guard.py` — zero-dependency CLI: scan a manifest.json (license/source/commercial/attribution), rate trainable + advice

```bash
python scripts/rights_guard.py --manifest manifest.json
python scripts/rights_guard.py --manifest manifest.json --json
```

### Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| "Just use the dataset" | Per-entry license/commercial gate |
| Manual license reading | Repeatable lexical check |
| Post-infringement cleanup | Pre-training exclusion, not after |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `doc-desens-scanner` and `ai-policy-radar`.

## 中文

把每条数据当带权属的资产：查许可证·商用权·署名·来源，缺许可的不进训练集。零依赖 `rights_guard.py`。

### 为什么比"抓来就训"强

| 痛点 | 本技能 |
|---|---|
| 爬来的数据，没写许可证 | 无许可证 → 排除 |
| 非商用数据被商用使用 | NC 标记 → 阻断商用 |
| 要求署名却没署名 | 标记，补全后方可使用 |
| "这数据哪来的？" | 来源可溯或隔离 |

### 包内有什么

- `SKILL.md` — 四信号权属模型 + 三步门禁 + 铁律
- `scripts/rights_guard.py` — 零依赖 CLI：扫描 manifest.json（license/source/commercial/attribution），评级可训练并给出建议

```bash
python scripts/rights_guard.py --manifest manifest.json
python scripts/rights_guard.py --manifest manifest.json --json
```

### 与同类工具对比

| 工具 | 本技能填补的空白 |
|---|---|
| "数据集直接用" | 逐条许可证/商用门禁 |
| 人工读许可证 | 可重复的词法检查 |
| 侵权后清理 | 训练前排除，而非事后 |

理论根基：**LGD 三律**（有籍·有证·有门禁）。与 `doc-desens-scanner`、`ai-policy-radar` 配对使用。

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

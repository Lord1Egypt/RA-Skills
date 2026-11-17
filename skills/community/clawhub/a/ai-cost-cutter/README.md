# ai-cost-cutter · AI 省钱跑批

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Stop burning money on LLM API calls. Four knives to cut cost: **batching** (off-peak / async 50% off), **local-model fallback** (cheap tasks run locally, flagships only for hard work), **cache layer** (never pay twice for the same request), **model routing** (pick model by task difficulty). Ships a runnable `cost_estimator.py` that turns task volume + prices into a monthly bill and the savings gap across 3 downgrade tiers. Born from the GOSIM entry *cross-machine-offline-taskbox* (offline batch on low-spec machines).

**中文** — 大模型不是越用越贵，是「怎么用」决定账单。四把刀降本：批处理 / 本地模型回退 / 缓存层 / 模型路由分级。附可运行成本估算脚本，输入任务量+单价即输出月度账单与三档降本方案的差额。源自 GOSIM 参赛作 cross-machine-offline-taskbox 的离线跑批思路。

## Why it beats "just use a cheaper model"

| Naive fix | Problem | This skill |
|---|---|---|
| Switch everything to cheap model | Quality collapses on hard tasks | Route by difficulty, keep flagship where it pays |
| Manually cache | Forgotten, inconsistent | Cache policy as a step in the flow |
| "Run at night" | No structure | Offline batch orchestration pattern |

## What's inside

- `SKILL.md` — 3 leak points + 4 knives + routing table + 铁律
- `scripts/cost_estimator.py` — zero-dependency CLI: baseline vs A/B/C tiers

```bash
python scripts/cost_estimator.py --calls 50000 --avg-in 800 --avg-out 400 \
    --price-flagship 0.01 --price-mid 0.003 --batch-disc 0.5 --local-frac 0.6
```

## Benchmark

| Approach | It does | Gap this fills |
|---|---|---|
| Provider pricing calculator | Single-model cost | No routing / batch / local mix |
| "Use local LLM" guides | Install Ollama | No decision rule on what to offload |
| This skill | Full cost architecture | Routes + batches + caches + offloads |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Companion to `context-engineering`.

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

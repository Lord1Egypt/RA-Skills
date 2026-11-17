# api-resilience · API 韧性

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — External APIs are *things that fail*. Wrap calls with exponential backoff + jitter, rate-limit counting, circuit breaker, and fallback — so one blip recovers instead of cascading. Ships a zero-dependency `resilience_demo.py`.

**中文** — 把外部调用当会失败的对象：指数退避+抖动重试、限流、熔断、降级，失败可恢复不雪崩。零依赖 `resilience_demo.py`。

## Why it beats "call it and pray"

| Pain | This skill |
|---|---|
| One 500 kills the chain | Backoff-retry, survives blips |
| 429 → retry storm | Rate-limit + jitter, no storm |
| Dep down, resources drained | Circuit breaker trips |
| No fallback, hard error | Degraded path returns兜底 |

## What's inside

- `SKILL.md` — 4-mechanism resilience + 3-step flow + 铁律
- `scripts/resilience_demo.py` — zero-dependency demo: backoff+jitter retry + circuit breaker with simulated failure/recover

```bash
python scripts/resilience_demo.py --fail-rate 0.6 --max-retry 5
python scripts/resilience_demo.py --fail-rate 0.9 --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Bare requests | No retry/breaker/fallback |
| Manual try/except | Ad-hoc, not standard pattern |
| "Retry immediately" | Backoff+jitter, no storm |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `agent-loop-guard` and `skill-quality-gate`.

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

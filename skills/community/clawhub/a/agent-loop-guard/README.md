# agent-loop-guard · 失控循环护栏

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — An agent run is a *controlled process*. Monitor step cap · repeated actions · no-progress, and trip a circuit breaker before it burns tokens spinning in place. Ships a zero-dependency `loop_guard.py`.

**中文** — 把 agent 运行当受控进程：监控步数上限·重复动作·状态无进展，触发即熔断并出诊断。零依赖 `loop_guard.py`。

## Why it beats "hope it terminates"

| Pain | This skill |
|---|---|
| Infinite A↔B loop | Repeated (tool,args) → trip |
| Re-clicking same tool | k identical calls → break |
| Token bill explodes | Step cap hard-stops |
| "Why did it loop?" | Trajectory + diagnosis saved |

## What's inside

- `SKILL.md` — 3-signal breaker + 3-step flow + 铁律
- `scripts/loop_guard.py` — zero-dependency CLI: read action trace, rate loop risk, suggest break + diagnosis

```bash
python scripts/loop_guard.py --trace trace.txt --max-steps 30 --repeat 3
python scripts/loop_guard.py --trace trace.txt --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| Manual timeout | Detects *repetition*, not just wall-clock |
| "Just set a timeout" | No per-step loop diagnosis |
| Post-hoc log scan | Real-time gate, stop before burn |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `skill-quality-gate` and `context-engineering`.

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

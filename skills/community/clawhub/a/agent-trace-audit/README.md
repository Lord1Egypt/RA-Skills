# agent-trace-audit

## English

Build an auditable action ledger for agent operations: timestamp, actor, action, object and gate status, enabling what-did-the-AI-do forensics and boundary audits.

This package is zero-dependency (Python stdlib only). See `SKILL.md` for the full bilingual procedure (English-first, Chinese-after) and `scripts/` for the CLI (`--help`).

---

## 中文

# agent-trace-audit · 智能体行为留痕审计

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — When an agent breaks, you must trace what it did. Build a ledger of ts · actor · action · target · gate, flag ungated (out-of-bounds) writes, emit timeline + violation list. Runnable `trace_audit.py`. Theoretical root: LGD — registered (fully traceable). Pairs with `agent-redteam-kit`.

**中文** — 把 agent 动作建成「时间戳·执行者·动作·对象·是否过闸」账本，标出越界操作，输出时间线+违规清单。附可运行脚本。理论根基：LGD 有籍。

## Why it beats "no log"

| Pain | This skill |
|---|---|
| Can't tell what agent did | Per-action ledger |
| Out-of-bounds write unseen | gate=ungated flagged red |
| Compliance can't prove control | Timestamped, read-only archive |

## What's inside

- `SKILL.md` — 5-field ledger + 3-step flow + 铁律
- `scripts/trace_audit.py` — zero-dependency CLI: build ledger from JSONL log

```bash
python scripts/trace_audit.py --log actions.jsonl
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| LangSmith/trace UI | Visual trace | No gate-violation flag, vendor lock |
| Print debugging | Ephemeral | Not archived, not auditable |
| "I think it did X" | — | No evidence |

Theoretical root: **LGD Three Laws** — registered. Pairs with `agent-redteam-kit`.

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

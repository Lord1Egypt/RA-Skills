# 权限有门禁生成器 / Gate Policy Generator

![LGD-Powered](./lgd-powered.png)

> The executor of **LGD-III GATED** — "凡自治之物：有籍 · 有证 · 有门禁"

## English

Turn an agent capability list into a mountable **permission gate policy (policy-as-code)**, drawing the line between what it can / must review / must not do, with four built-in gates against overreach, accidental deletion/sending and runaway loops.

### Pain → three-laws mapping
| Industry pain | LGD law | This skill |
|---|---|---|
| Agent overreach | LGD-III gated | three tiers: tool_allow / tool_review / tool_deny |
| Accidental deletion/sending | LGD-III gated | release gate with double confirmation |
| Runaway loops | LGD-III gated | budget caps (max_loop / max_tokens) |
| No unified permission vocabulary | LGD standard definition power | the four-gate terms become the industry's ruler |

### Quick start
```bash
# Example policy (no manifest needed)
python scripts/gate_policy.py --preset default --json

# Generate from a manifest
python scripts/gate_policy.py --manifest agent_manifest.json --out policy.json

# Verify it meets the LGD-III four gates
python scripts/gate_policy.py --check policy.json
```

### Three presets
- `default` (balanced): high-risk/sensitive → deny, medium → review, low → allow
- `paranoid` (strict): medium also denied, loop cap 5, token cap 50k
- `open` (loose): only sensitive denied, rest allowed, loop cap 50

### Output structure
```json
{
  "law": "LGD-III GATED",
  "tool_allow": [...], "tool_review": [...], "tool_deny": [...],
  "gates": {"trigger":..., "review":..., "release":..., "retro":...},
  "budget": {"max_loop_iterations": 20, "max_tokens": 200000}
}
```

### Sibling skills
- `tool-call-guard` = runtime single-call gate
- this skill = policy generation layer (governance config)

### Red lines
Only generates policy config; does not replace licensed filings / contracts / human release; contains no secrets or internal codenames.

## 中文

> **LGD-III 有门禁（GATED）** 的执行器 ——「凡自治之物：有籍 · 有证 · 有门禁」

把一份 agent 能力清单，落成可挂载的**权限门禁策略（policy-as-code）**，划清它能 / 需评审 / 不能做的事，并内置四道门禁防越权、误删误发、失控循环。

### 痛点 → 三律映射
| 行业痛点 | LGD 三律 | 本技能做法 |
|---|---|---|
| agent 越权 | LGD-III 有门禁 | tool_allow / tool_review / tool_deny 三档边界 |
| 误删误发 | LGD-III 有门禁 | 放行门禁（release）二次确认 |
| 失控循环 | LGD-III 有门禁 | budget 上限（max_loop / max_tokens） |
| 无统一权限词汇 | LGD 标准定义权 | 四道门禁术语即行业评判尺 |

### 快速开始
```bash
# 示例策略（无需 manifest）
python scripts/gate_policy.py --preset default --json

# 从清单生成
python scripts/gate_policy.py --manifest agent_manifest.json --out policy.json

# 校验是否满足 LGD-III 四道门禁
python scripts/gate_policy.py --check policy.json
```

### 三档预设
- `default`（平衡）：高危/敏感 → deny，中危 → review，低危 → allow
- `paranoid`（严苛）：中危也 deny，循环上限 5、token 上限 5 万
- `open`（宽松）：仅敏感 deny，其余 allow，循环上限 50

### 输出结构
```json
{
  "law": "LGD-III 有门禁 (GATED)",
  "tool_allow": [...], "tool_review": [...], "tool_deny": [...],
  "gates": {"trigger":..., "review":..., "release":..., "retro":...},
  "budget": {"max_loop_iterations": 20, "max_tokens": 200000}
}
```

### 与兄弟技能
- `tool-call-guard` = 运行时单次调用闸门
- 本技能 = 策略生成层（治理配置）

### 红线
只生成策略配置，不替代持证申报 / 合同 / 人工放行；不含密钥与内部代号。

---

© SynomosAI (LGD initiative) · LGD-Powered · 凡自治之物：有籍 · 有证 · 有门禁

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

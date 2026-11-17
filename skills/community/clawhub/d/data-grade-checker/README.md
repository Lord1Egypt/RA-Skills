# data-grade-checker · 数据分类分级判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.


## What it does
Classifies data into 核心数据 / 重要数据 / 一般数据 per **GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)** (pending manual verification; official texts prevail).

- **Insufficient input → strict presumption (从严推定)**: with `core_interest` (or industry/scale) missing, the tool returns the **most obligation-heavy grade** among the possible ones, states the possible range in `warnings`, and sets `rc=1`. It never silently returns 「一般数据」.
- **No silent invalid input**: non-yes/no `core_interest`/`cross_border`, non-high/mid/low `scale` → gate error (`rc=2`).
- **Out of scope**: industry-specific sensitive-data catalogues, personal-information dimension, full cross-border filing process.

## Install & run (zero-dependency, Python 3.8+)
```bash
python data-grade-checker.py --demo   # 3 built-in smoke cases
# rc=1 (strict presumption, no args)
python data-grade-checker.py
# rc=0 (complete args → 一般数据)
python data-grade-checker.py --industry retail --core_interest no --scale low
# rc=2 (invalid input)
python data-grade-checker.py --industry retail --scale huge
```

## Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `industry` | no | 行业：finance/energy/transport/bio/health/geo/population/gov/key_infra 等 |
| `core_interest` | no | 是否涉及国家核心利益：yes/no |
| `scale` | no | 规模/敏感度：high/mid/low |
| `cross_border` | no | 是否出境：yes/no |

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = invalid input), `grade`, `obligations`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real excerpt (`--demo` case 2, values verbatim):

```json
{
  "input": {"industry": "finance", "scale": "high"},
  "result": {
    "grade": "核心数据",
    "obligations": ["出境安全评估 + 审批", "最高级保护义务", "原则上不得出境"],
    "warnings": [
      "输入不完整：未说明是否涉及国家核心利益（core_interest），该参数可触发最高级；建议补齐 core_interest / industry / scale 后复核。",
      "分级不确定（可能区间 重要数据～核心数据）：已按从严推定取『核心数据』（义务最重者），实际等级可能更宽松；请补齐参数后复核。"
    ]
  },
  "rc": 1
}
```

## Rule-source review checklist (pending manual verification)
| Clause | Used for | Status |
|---|---|---|
| GB/T 43697-2024 | 核心/重要/一般数据分级规则来源 | 待人工核对 |
| 行业敏感清单 | 重要数据行业判定 | 待人工核对 |
| core_interest=yes → 核心数据 | 最高级触发条件 | 待人工核对 |
| 跨部门按就高原则 | 多属性数据定级 | 待人工核对 |

## Theory hook
数据须有籍、有级、有门禁——分类分级即数字世界的产权登记。域站位件：TH-DAT-001。

## Pointers
- LGD 理论总账 REGISTRY 在线页：(地址待补) · DAT 域速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `data-grade-checker.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, the 「理论依据」 section and all theory wording | **Not covered by MIT**: all rights reserved |

> 代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。

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
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**。）
**本包补充**：`data-grade-checker.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。中文文档见 `SKILL.md`。

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |

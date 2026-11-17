# aut-grade-checker · 车辆驾驶自动化等级判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

[![LGD-Powered](（外部链接待补） 理论页链接待补）)

## What it does
Classifies driving-automation level L0–L5 per **GB/T 40429-2021《汽车驾驶自动化分级》表1** (pending manual verification; official texts prevail) from four axes: `dd` / `oedr` / `odd_limited` / `takeover_needed` (+ `both_axes` for L1/L2).

- **Insufficient input → strict presumption (从严推定)**: missing optional axes return the **most obligation-heavy grade** among the possible ones, state the possible range in `warnings`, and set `rc=1`. It never silently returns a lenient grade.
- **No silent invalid input**: out-of-enum values (e.g. `--dd banana`) → gate error (`rc=2`).
- **Out of scope**: type approval, accident liability, regional regulations.

## Install & run (zero-dependency, Python 3.8+)
```bash
python aut-grade-checker.py --demo   # 2 built-in smoke cases
# rc=1 (strict presumption, incomplete input)
python aut-grade-checker.py --dd system --oedr system
# rc=0 (complete args → L2)
python aut-grade-checker.py --dd vehicle --oedr driver --both_axes yes
# rc=2 (invalid input)
python aut-grade-checker.py --dd banana --oedr system
```

## Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `dd` | yes | 动态驾驶任务执行方：system/vehicle/driver（vehicle 视作 system） |
| `oedr` | yes | 目标事件探测响应方：system/driver |
| `odd_limited` | no | 是否限定 ODD：yes/no |
| `takeover_needed` | no | 是否需人工接管：yes/no |
| `both_axes` | no | 是否同时执行转向+加减速：yes/no（L1/L2 区分） |

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `grade`, `responsibility`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real output (`--dd system --oedr system`, values verbatim):

```json
{
  "result": {
    "grade": "L5",
    "responsibility": "系统在所有ODD执行全部DD+OEDR，无限制",
    "warnings": [
      "输入不完整：odd_limited/takeover_needed 未提供（官方分级同时使用 ODD 限定与接管要求），建议补齐后复核。",
      "分类不确定（可能等级区间 L3～L5）：odd_limited/takeover_needed 参数不足，已按从严推定取『L5』（义务最重者），实际等级可能更宽松；请补齐参数后复核。",
      "L3+ 不得宣称'自动驾驶/L2.9'等误导级别（'L2.9级'乱象可直接据此判定）"
    ]
  },
  "rc": 1
}
```

## Rule-source review checklist (pending manual verification)
| Clause | Used for | Status |
|---|---|---|
| GB/T 40429-2021 表1 | 0-5 级分级判定（DD/OEDR/ODD/接管四要素） | 待人工核对 |
| 'vehicle 视作 system' 口径 | dd/oedr 参数归一化 | 待人工核对 |
| L3+ 告警口径 | 不得宣称'自动驾驶/L2.9'等误导级别 | 待人工核对 |

## Theory hook
自治的边界须被标注——分级即把'谁在开车'写进责任契约。域站位件：TH-AUT-001。

## Pointers
- LGD theory page: （LGD 理论页链接待补） · Skill library: （外部技能库链接待补） · llms.txt: （llms.txt 链接待补）
- LGD 理论总账 REGISTRY 在线页：(地址待补) · AUT 域速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `aut-grade-checker.py` | **MIT** |
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
**本包补充**：`aut-grade-checker.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。中文文档见 `SKILL.md`。

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |

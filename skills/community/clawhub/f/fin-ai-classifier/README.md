# fin-ai-classifier · 金融 AI 应用分级判定器 / Financial AI Application Tiering Classifier

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

## English

### What it does
Classifies financial AI applications into I/II/III risk grades per the **TH-FIN-002 master (FDA SaMD tiering thinking adapted to finance) + financial-AI regulatory guidance** (pending manual verification; the latest regulatory guidance prevails).

- **Insufficient input → strict presumption**: with `autonomy`/`impact` missing, the tool returns the **most obligation-heavy grade** among the possible ones, states the possible range in `warnings`, and sets `rc=1`. It never silently returns Grade I (low risk).
- **No silent invalid input**: out-of-enum values → gate error (`rc=2`).
- **Out of scope**: licensing status, filing material lists, algorithm-filing workflow.

### Install & run (zero-dependency, Python 3.8+)
```bash
python fin-ai-classifier.py --demo   # 2 built-in smoke cases
# rc=1 (strict presumption, no args)
python fin-ai-classifier.py
# rc=0 (complete args → Grade I)
python fin-ai-classifier.py --autonomy info --impact low
# rc=2 (invalid input)
python fin-ai-classifier.py --autonomy full --impact extreme
```

### Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `autonomy` | no* | Autonomy: full / human_in_loop / info (defaults to strict presumption) |
| `impact` | no* | Impact: high / mid / low (defaults to strict presumption) |
| `target` | no | Object: consumer / institution |

\* Semantically key tiering parameters; when missing, the tool outputs the strict-presumption conclusion with a warning, without blocking execution.

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = invalid input), `grade`, `obligations`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata).

```json
{
  "input": {"autonomy": null, "impact": null, "target": null},
  "result": {
    "grade": "Grade III (high risk)",
    "obligations": ["algorithm filing", "human fallback + explainability", "model & data compliance audit", "regulatory reporting"],
    "warnings": [
      "Incomplete input: no autonomy / impact given; review after completing.",
      "Tier uncertain (possible range Grade I–III): strict presumption took Grade III (heaviest obligations); actual grade may be lighter; review after completing parameters."
    ]
  },
  "rc": 1
}
```

### Rule-source review checklist (pending manual verification)
| Clause | Used for | Status |
|---|---|---|
| TH-FIN-002 master | I/II/III tiering framework | pending manual check |
| full + high → Grade III | Highest-grade trigger | pending manual check |
| human_in_loop + high/mid → Grade II | Mid-risk trigger | pending manual check |
| Algorithm filing (per public-opinion attributes) | Grade II obligation reference | pending manual check |
| No-licensed AI stock-recommendation / lending | Grade III warning basis | pending manual check |

### Theory hook
Financial autonomy must be tiered — tiering nails "can the AI decide for you" onto the regulatory coordinate system. Domain slot: TH-FIN-002.

## 中文

### 它做什么
依据 **TH-FIN-002 母版（FDA SaMD 分级思维平移金融）+ 金融AI监管导向**（待人工核对；以最新监管口径为准）将金融 AI 应用分为 I/II/III 风险级。

- **输入不足 → 从严推定**：缺 `autonomy`/`impact` 时返回可能区间中**义务最重的级**，在 `warnings` 中说明可能区间，置 `rc=1`，绝不静默返回 I 级（低风险）。
- **无效输入不静默**：枚举外取值 → 门禁错误（`rc=2`）。
- **不做什么**：牌照状态、备案材料清单、算法备案流程。

### 安装与运行（零依赖，Python 3.8+）
```bash
python fin-ai-classifier.py --demo   # 2 个内置冒烟用例
python fin-ai-classifier.py                       # rc=1（从严推定，无参数）
python fin-ai-classifier.py --autonomy info --impact low   # rc=0（参数齐 → I 级）
python fin-ai-classifier.py --autonomy full --impact extreme  # rc=2（非法输入）
```

### 参数
| 参数 | 必填 | 含义 |
|---|---|---|
| `autonomy` | 否* | 自主度：full/human_in_loop/info（缺省按从严推定） |
| `impact` | 否* | 影响：high/mid/low（缺省按从严推定） |
| `target` | 否 | 对象：consumer/institution |

\* 语义上为分级关键参数；缺省时输出从严推定结论并告警，不阻塞执行。

### 输出
确定性 JSON IR，含 `rc`（**0**=ok / **1**=完成有告警 / **2**=非法输入）、`grade`、`obligations`、`warnings` 与 `aigc_mark`（GB 45438-2025 元数据）。

### 规则源待人工核对清单
| 条款 | 用途 | 状态 |
|---|---|---|
| TH-FIN-002 母版 | I/II/III 级分级框架 | 待人工核对 |
| full + high → III 级 | 最高级触发条件 | 待人工核对 |
| human_in_loop + high/mid → II 级 | 中风险级触发条件 | 待人工核对 |
| 算法备案（依舆论属性） | II 级义务引用 | 待人工核对 |
| 禁止 AI 荐股/放贷无资质经营 | III 级告警依据 | 待人工核对 |

### 理论钩子
金融的自治须有级——分级即把"AI 能否替你做决定"钉进监管坐标。域站位件：TH-FIN-002。

---

## License & attribution
**分层许可——代码许可不覆盖文档与理论文本。**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `fin-ai-classifier.py` | **MIT** |
| 文档与理论文本 | 本 `README.md`、`SKILL.md`、「理论依据」部分及一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利 |

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
**本包补充**：`fin-ai-classifier.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |

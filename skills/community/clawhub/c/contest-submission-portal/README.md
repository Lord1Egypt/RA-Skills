# contest-submission-portal · 赛事作品提交合规校验器

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with organizing committee. Text verified: 2026-09-26.

[![LGD-Powered](（外部链接待补） 理论页链接待补）)

## What it does
Validates submission completeness & format per **UIBC 赛事提交规范（四规范·提交章）v0.1** (pending manual verification; the latest UIBC charter prevails).

- Tracks: `code` (.uibc + seal.json + AIGC 声明 + RUN.md) / `theory` (paper + 最小可执行示例) / `design` (方案 + 失败模式分析).
- **No silent pass**: missing `format` → warning "未做白名单校验" (`rc=1`); unknown `track` → gate error (`rc=2`), never a fake checklist.
- Executables (`.exe/.dll/.bat/.ps1/.so/.bin`) → rejected.

## Install & run (zero-dependency, Python 3.8+)
```bash
python contest-submission-portal.py --demo   # 3 built-in smoke cases
# rc=0 (all required items present)
python contest-submission-portal.py --track code --files "submission.uibc,seal.json,aigc-declaration.md,RUN.md,attack-report.md" --format py
# rc=1 (missing items + bad format)
python contest-submission-portal.py --track code --files "solution.py,readme.md" --format exe
# rc=2 (unknown track)
python contest-submission-portal.py --track music --files "a.md" --format md
```

## Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `track` | yes | 赛道：code/theory/design |
| `files` | no | 提交文件清单（逗号分隔） |
| `format` | no | 主文件格式（缺省时白名单不做判定并告警） |

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `required`, `provided`, `missing`, `valid`, `format_ok`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real excerpt (`--demo` case 1, values verbatim):

```json
{
  "input": {"track": "code", "files": "submission.uibc,seal.json,aigc-declaration.md,RUN.md,attack-report.md", "format": "py"},
  "result": {
    "required": ["uibc-package", "seal", "aigc", "run"],
    "missing": [],
    "valid": true,
    "format_ok": true,
    "warnings": [],
    "evidence": ["UIBC 赛事提交规范·提交章 v0.1"]
  },
  "rc": 0
}
```

## Rule-source review checklist (pending manual verification)
| Rule | Used for | Status |
|---|---|---|
| 提交章 v0.1 必交项清单 | 各赛道完整性校验 | 待人工核对 |
| 格式白名单 code/theory/design | 主文件格式校验 | 待人工核对 |
| 禁止可执行二进制 | 提交门禁直接退回 | 待人工核对 |

## Theory hook
公平始于可核验的入口——提交校验即把'谁在参赛'钉进可信起点。域站位件：TH-EVT-001。

## Pointers
- LGD theory page: （LGD 理论页链接待补） · Skill library: （外部技能库链接待补） · llms.txt: （llms.txt 链接待补）
- LGD 理论总账 REGISTRY 在线页：(地址待补) · 赛事线速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `contest-submission-portal.py` | **MIT** |
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
**本包补充**：`contest-submission-portal.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。中文文档见 `SKILL.md`。

## 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |

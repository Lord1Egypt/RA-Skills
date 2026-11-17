# anti-cheat-identity · 赛事反作弊身份核验器

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with organizing committee. Text verified: 2026-09-26.

[![LGD-Powered](（外部链接待补） 理论页链接待补）)

## What it does
Verifies submitter identity / environment consistency per **UIBC 反作弊规范 + 通用学术诚信原则** (thresholds pending manual verification; the latest UIBC charter prevails).

- Risk tiers: `low` (放行) / `mid` (人工抽检) / `high` (冻结通道并人工核查；冻结≠撤销).
- **No silent defaults on invalid input**: non-numeric `submit_count` / `time_gap_min`, negative values, or a non-JSON-array `prev_env_hashes` → gate error (`rc=2`), never a lenient default.

## Install & run (zero-dependency, Python 3.8+)
```bash
python anti-cheat-identity.py --demo   # 2 built-in smoke cases
# rc=0 (low risk)
python anti-cheat-identity.py --author_id teamA --env_hash abc123 --prev_env_hashes '["abc123"]' --submit_count 1 --time_gap_min 120
# rc=1 (completed with warnings)
python anti-cheat-identity.py --author_id teamB --env_hash xyz999 --prev_env_hashes '["a1","a2","a3","a4","a5"]' --submit_count 8 --time_gap_min 3
# rc=2 (invalid input)
python anti-cheat-identity.py --author_id teamC --env_hash h1 --submit_count abc
```

## Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `author_id` | yes | 作者标识 |
| `env_hash` | yes | 环境指纹哈希 |
| `prev_env_hashes` | no | 历史环境指纹 JSON 数组字符串 |
| `submit_count` | no | 同作者提交次数（正整数，默认 1） |
| `time_gap_min` | no | 距上次提交分钟（非负数字，默认按无间隔信息处理） |

## Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `risk_level`, `flags`, `advice`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real excerpt (`--demo` case 2, values verbatim):

```json
{
  "tool": "anti-cheat-identity",
  "input": {"author_id": "teamB", "env_hash": "xyz999",
            "prev_env_hashes": "[\"a1\",\"a2\",\"a3\",\"a4\",\"a5\"]",
            "submit_count": "8", "time_gap_min": "3"},
  "result": {
    "risk_level": "high",
    "flags": ["环境指纹与历史不一致（疑似换设备/环境）", "历史环境指纹过多（疑似多环境轮换）",
              "同作者提交次数过高(8)", "相邻提交间隔过短(3分钟)"],
    "advice": "高风险：冻结提交通道并人工核查（冻结≠撤销，处置记录须留痕）",
    "warnings": ["…与 flags 相同 4 条"]
  },
  "rc": 1
}
```

## Rule-source review checklist (pending manual verification)
| Rule / threshold | Used for | Status |
|---|---|---|
| UIBC 反作弊规范 | 环境指纹一致性 / 多环境轮换判定口径 | 待人工核对 |
| 历史指纹 >3 个 | 「疑似多环境轮换」触发线 | 待人工核对 |
| 同作者提交 >5 次 | 「提交次数过高」触发线 | 待人工核对 |
| 相邻间隔 <10 分钟 | 「间隔过短」触发线 | 待人工核对 |

## Theory hook
可信始于身份——环境一致性核验即把'谁在参赛'锁进防作弊的围栏。域站位件：TH-EVT-004。

## Pointers
- LGD theory page: （LGD 理论页链接待补） · Skill library: （外部技能库链接待补） · llms.txt: （llms.txt 链接待补）
- 理论总账 REGISTRY 在线页：(地址待补) · 赛事线速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `anti-cheat-identity.py` | **MIT** |
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
**本包补充**：`anti-cheat-identity.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。中文文档见 `SKILL.md`。

## 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |

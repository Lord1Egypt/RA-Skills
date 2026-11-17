# evid-four-check · 电子证据四性审查判定器 / Electronic Evidence Four-Properties Review

> AI-assisted decision-support CLI. **NOT legal advice**, **not a legal conclusion** — verify against official texts. Text verified: 2026-09-26.

## English

### What it does
Reviews electronic evidence on the four properties — authenticity / legality / relevance / integrity — per official rules: **Supreme People's Court *Provisions on Several Issues Concerning Evidence in Civil Procedures*, Articles 14, 93–95, plus *Rules of the People's Courts on Online Litigation*, Articles 12–18** (clause numbers **pending manual verification** — see `clause_review_checklist` in the output; official texts prevail).

- **Insufficient input → strict presumption**: any dimension that cannot be determined because an argument is missing is judged **FAIL (to be reinforced)** — the most obligation-heavy outcome among the possible ones. The tool states the **possible range** and how to supply the missing argument in `warnings`, and sets `rc=1`. It never silently returns a lenient (PASS) conclusion. `dimension_basis` marks each dimension as `明确输入` (explicit input) or `从严推定（输入不完整）` (strict presumption, incomplete input).
- **Out of scope**: substantive review of the **legality of the collection method** (the tool's "legality" is a formal check only — was an evidence type declared), admissibility / probative-weight judgment, notarisation & expert-opinion effect, cross-examination and spoliation (Art. 95) discretion, foreign / criminal / administrative rules, physical verification of originals.

### Install & run (zero-dependency, Python 3.8+)
```bash
python evid-four-check.py --demo                          # 3 built-in smoke cases (rc=0 / rc=1 / rc=1)
python evid-four-check.py --type electronic-contract --has_signature yes \
  --source_verifiable yes --integrity_check yes --relevance yes   # complete args, all PASS → rc=0
python evid-four-check.py --type chat-log --has_signature no \
  --integrity_check no --relevance yes                    # source_verifiable missing → strict presumption, rc=1
python evid-four-check.py --relevance maybe                # invalid value → rc=2
```

| Argument | Meaning | Values | `required` in META |
|---|---|---|---|
| `--type` | evidence type (drives the "legality" formal check) | contract / chat-log / email / log / audio-video … | `False` |
| `--has_signature` | digital signature / trusted timestamp / blockchain notarisation | `yes` / `no` | `False` |
| `--source_verifiable` | source verifiable (traceable to original carrier/system) | `yes` / `no` | `False` |
| `--integrity_check` | integrity hash / original-carrier comparison done | `yes` / `no` | `False` |
| `--relevance` | relevant to the fact to be proved | `yes` / `no` | `False` |

All five arguments are optional — **at least one** is required; argparse reads each `required` field from META (metadata and behaviour agree). Any other value than `yes`/`no` (also accepted: `y/n`, `true/false`, `1/0`, `是/否`, `有/无`) → `rc=2`. Output is always JSON IR (indented); there is **no output-format switch** — the legacy ghost flag `--json` was removed.

### Output
Deterministic JSON IR with `rc` (**0** = completed, no warnings / **1** = completed with warnings, incl. strict presumption / **2** = insufficient or invalid input), `four_properties`, `dimension_basis`, `possible_conclusions`, `conclusion`, `remediation`, `missing_inputs`, `warnings`, `clause_review_checklist`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

```json
{
  "tool": "evid-four-check",
  "input": {"type": "chat-log", "has_signature": "no", "source_verifiable": null,
            "integrity_check": "no", "relevance": "yes"},
  "result": {
    "four_properties": {"authenticity": "FAIL", "legality": "PASS", "relevance": "PASS", "integrity": "FAIL"},
    "dimension_basis": {"authenticity": "strict presumption (incomplete input)", "legality": "explicit input",
                        "relevance": "explicit input", "integrity": "explicit input"},
    "conclusion": "Some four-property formal checks failed; evidentiary capacity to be reinforced (not an admission or weight conclusion; final admission is decided by the judicial authority)",
    "missing_inputs": ["source_verifiable"],
    "warnings": ["… 5 warnings total (strict presumption / possible range / how to supply missing args / explicit failures / formal-review disclaimer)"]
  },
  "rc": 1,
  "clause_review_checklist": ["… 7 items total (clause number + purpose + pending manual check)"],
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "evid-four-check@SynomosAI",
                "content_type": "decision_support_output", "label_note": "label basis pending verification"}
}
```
(Arrays trimmed and marked `…`; values verbatim from the tool.)

### Theory hook (evidence-semantics clarification)
Evidence must be accountable — four-properties review writes "trust" into every act of proof. Per the LGD evidence semantics: **Evidence = a verifiable basis for a governance-state transition, not a behaviour log**; the `evidence` in the output is **rule provenance (clause basis)**, not the case evidence ledger. Domain slot: TH-LAW-001.

### Clause review checklist (pending manual verification)
| Clause / scope | Purpose | Status |
|---|---|---|
| Evidence Provisions Art. 14 | Scope definition of electronic data | pending manual check |
| Evidence Provisions Art. 93 | Factors for authenticity review of electronic data | pending manual check |
| Evidence Provisions Art. 94 | Authenticity presumption situations (third-party notarisation, neutral systems, notarisation, etc.) | pending manual check |
| Evidence Provisions Art. 95 | Consequences of a party controlling evidence and refusing to submit (obstruction of proof) | pending manual check |
| Online Litigation Rules Arts. 12–18 | Submission of electronic materials, original-document determination, blockchain notarisation and on-chain authenticity review in online litigation (range pending) | pending manual check |
| GB 45438-2025 | AIGC label field `aigc_mark` | pending manual check |
| "Four properties" dimension split (authenticity/legality/relevance/integrity) | This tool's output structure; a review-checklist convention, **not the wording of any statute** | pending manual check |

### Pointers (unverified — links pending)
- Theory ledger repo: https://github.com/zhaoxinghua09-cell/lgd-theory
- Reference implementation: https://github.com/zhaoxinghua09-cell/uibc-core
- Skill library index: https://github.com/zhaoxinghua09-cell/agent-skills

## 中文

### 它做什么
依据官方规则对电子证据做四性审查——真实性 / 合法性 / 关联性 / 完整性：**最高人民法院《关于民事诉讼证据的若干规定》第14条、第93-95条 + 《人民法院在线诉讼规则》第12-18条**（条款号**待人工核对**——见输出中的 `clause_review_checklist`；以官方文本为准）。

- **输入不足 → 从严推定**：任何因参数缺失而无法判定的维度，一律判 **FAIL（待补强）**——这是可能结论中义务最重的一档。工具在 `warnings` 中给出**可能区间**及如何补齐缺失参数，并置 `rc=1`。它绝不悄悄返回宽松（PASS）结论。`dimension_basis` 将每个维度标记为 `明确输入` 或 `从严推定（输入不完整）`。
- **不做什么**：对**取证手段合法性**的实质审查（本工具的「合法性」仅为形式检查——是否声明了证据类型）、可采性/证明力判断、公证与鉴定效力、质证与证明妨碍（第95条）裁量、涉外/刑事/行政规则、原件的物理核验。

### 安装与运行（零依赖，Python 3.8+）
```bash
python evid-four-check.py --demo                          # 3 个内置冒烟用例（rc=0 / rc=1 / rc=1）
python evid-four-check.py --type 电子合同 --has_signature yes \
  --source_verifiable yes --integrity_check yes --relevance yes   # 参数齐全，全 PASS → rc=0
python evid-four-check.py --type 聊天记录 --has_signature no \
  --integrity_check no --relevance yes                    # 缺 source_verifiable → 从严推定，rc=1
python evid-four-check.py --relevance maybe                # 非法取值 → rc=2
```

| 参数 | 含义 | 取值 | META 中 `required` |
|---|---|---|---|
| `--type` | 证据类型（驱动「合法性」形式检查） | 合同 / 聊天记录 / 邮件 / 日志 / 音视频 … | `False` |
| `--has_signature` | 数字签名 / 可信时间戳 / 区块链存证 | `yes` / `no` | `False` |
| `--source_verifiable` | 来源可核验（可追溯至原始载体/系统） | `yes` / `no` | `False` |
| `--integrity_check` | 完整性哈希 / 与原始载体比对完成 | `yes` / `no` | `False` |
| `--relevance` | 与待证事实相关 | `yes` / `no` | `False` |

五个参数均可选——**至少给一个**；argparse 从 META 读取每个 `required` 字段（元数据与行为一致）。取 `yes`/`no` 之外的值（亦接受 `y/n`、`true/false`、`1/0`、`是/否`、`有/无`）→ `rc=2`。输出恒为 JSON IR（缩进）；**没有输出格式开关**——遗留幽灵参数 `--json` 已移除。

### 输出
确定性 JSON IR，含 `rc`（**0** = 完成无告警 / **1** = 完成有告警，含从严推定 / **2** = 输入不足或非法）、`four_properties`、`dimension_basis`、`possible_conclusions`、`conclusion`、`remediation`、`missing_inputs`、`warnings`、`clause_review_checklist`，以及 `aigc_mark`（GB 45438-2025 元数据；`is_generated: true`，标识口径标注待核）。

### 理论钩子（证据语义澄清）
证据须可被问责——四性审查即把「可信」写进每一次举证。依 LGD 证据语义界定：**Evidence（证据）＝治理状态转换的可验证依据，非行为日志**；输出中的 `evidence` 是**规则出处（条款依据）**，不是本案证据台账。域站位件：TH-LAW-001。

### 条款号待人工核对清单
| 条款 / 口径 | 用途 | 状态 |
|---|---|---|
| 证据规定 第14条 | 电子数据范围的界定 | 待人工核对 |
| 证据规定 第93条 | 电子数据真实性审查的考虑因素 | 待人工核对 |
| 证据规定 第94条 | 真实性推定情形（第三方平台存证、中立系统、公证等） | 待人工核对 |
| 证据规定 第95条 | 一方控制证据而拒不提交的法律后果（举证妨碍） | 待人工核对 |
| 在线诉讼规则 第12条～第18条 | 在线诉讼中电子化材料的提交、原件认定、区块链存证与上链真实性审查（区间范围待核） | 待人工核对 |
| GB 45438-2025 | AIGC 标识字段 `aigc_mark` | 待人工核对 |
| 「四性」维度划分（真实/合法/关联/完整） | 本工具输出结构；属审查清单口径，**非任何条文原文表述** | 待人工核对 |

### 链接（未核验——地址待补）
- 理论总账仓：https://github.com/zhaoxinghua09-cell/lgd-theory
- 参考实现：https://github.com/zhaoxinghua09-cell/uibc-core
- 技能库索引：https://github.com/zhaoxinghua09-cell/agent-skills

---

## License & attribution
**分层许可——代码许可不覆盖文档与理论文本。**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `evid-four-check.py` | **MIT** |
| 文档与理论文本 | 本 `README.md`、`SKILL.md`、「理论依据」部分及一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利 |

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**。）
**本包补充**：`evid-four-check.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。

## 家族合集
| 域 | 工具 | 大使 | 目录 |
|---|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/uas-ops-checker |
| AUT 驾驶 | aut-grade-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/aut-grade-checker |
| DAT 数据 | data-grade-checker | 诺源 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/data-grade-checker |
| BIO 生物 | hgrac-route-checker | 诺康 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/hgrac-route-checker |
| FIN 金融 | fin-ai-classifier | 诺丰 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/fin-ai-classifier |
| LAW 法律 | evid-four-check | 诺律 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evid-four-check |

---
诺律@LAW 域首席发声人 · TH-LAW-001 · SynomosAI（AI 辅助生成，非自然人）

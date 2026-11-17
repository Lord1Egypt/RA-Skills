# cer-equivalence-check

## English

Deterministic zero-dependency CLI screener for medical-device compliance (cer-equivalence-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts.

This package is zero-dependency (Python stdlib only). See `SKILL.md` for the full bilingual procedure (English-first, Chinese-after) and `scripts/` for the CLI (`--help`).

---

## 中文

# cer-equivalence-check · 临床评价报告等同性论证要素检查器

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> Zero-dependency deterministic CLI screener for medical-device compliance.
> **Decision support only — NOT legal/regulatory advice. Always verify against official texts.** Text verified: 2026-09-26.

## Why

临床评价选了等同器械这条捷径，结果被问「数据访问权在哪」——要素缺一项，整条路走不通。

## What it does

Screens `cer-equivalence-check` against public rule sources: **MDR (EU) 2017/745 Art 61 + Annex XIV Part A / MDCG 2020-5、2020-6 / MEDDEV 2.7/1 rev.4**.
Outputs deterministic JSON IR with `rc` (0 = ok / 1 = ok with warnings / 2 = insufficient input),
`error_code`, and GB 45438-2025 AIGC metadata. No network, no API key, no third-party packages.

- **Insufficient input → strict presumption**: missing CER sections and a missing data-access contract are both spelled out in `warnings` (`rc=1`) — never silently treated as "complete".
- Measured: all ten args `yes` → rc=0; `--is_equivalent yes` alone → rc=1 (access-right + missing-section warnings); `--has_plan yes` alone (no `--is_equivalent`) → rc=2.

## Run it (Python 3.8+)

```bash
python cer-equivalence-check.py --demo
python cer-equivalence-check.py --json <your args...>
```

## Compliance & IP

- Author: SynomosAI contributors · © 2026 SynomosAI · MIT License
- Theory anchor: `TH-MED-009` (LGD · registry / evidence / gate)
- Published by an AI-assisted studio; the institution bears responsibility for the output.
- Online (Chinese): https://synomos.ai

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `cer-equivalence-check.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在代码许可覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依其自身许可使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 SynomosAI contributors · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块：**A 段公共段逐字复制、未删改；B 段资产参数段按本包真值填写**；发布 / 重提前须照最新版本复核。）

## Family

| 环节 | 工具 | 位置 |
|---|---|---|
| 分类与路径 | `md-classification-route` | 本批 |
| 注册资料-技术文件 | `medxpert-reg-hub` | 存量枢纽 |
| 临床评价（选路） | `clin-eval-route-picker` | 存量 |
| 临床评价（证据要素） | `cer-equivalence-check` | 本批 |
| 检测项目与实验室匹配 | `test-lab-match-check` | 本批 |
| 申报前非临床研究 | `non-clinical-checker` | 存量 |
| UDI（格式校验） | `udi-format-validator` | 存量 |
| UDI（数据库提交） | `udi-db-submission-check` | 本批 |
| 上市后·PMCF 计划 | `pmcf-plan-check` | 存量 |
| 上市后·PMCF 评价报告 | `pmcf-evaluation-report-check` | 本批 |
| 上市后·不良事件 | `pms-vigilance-intake` | 存量 |
| 上市后·召回 | `recall-decision-checker` | 存量 |
| 标签与说明书 | `label-compliance-checker` | 存量 |
| 进出口路径 | `import-export-router` | 存量 |

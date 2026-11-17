# 合同高危条款扫描器 / Contract Clause Check

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `contract-clause-check` v1.0.0 · LGD Moat Family · Zero-dependency · Domain: 法律 · Law-map: TH-LGD-022

**中文**：合同不看条款直接签，违约金30%、单方解释权、没写管辖全踩坑 一条命令完成初筛：合规 PASS（rc=0）/ 违规 FAIL（rc=1）/ 用法错误（rc=2），支持 `--json`。

**EN**: One-command pre-screening for 法律. PASS (rc=0) / FAIL (rc=1) / usage error (rc=2). `--json` supported.

## Usage / 用法
```bash
python scripts/contract_clause_check.py --help
```

## Disclaimer / 免责
Screening aid only, not legal/investment/medical advice. / 合规初筛辅助，不构成专业意见。

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
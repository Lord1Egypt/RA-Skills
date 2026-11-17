# 文档合规处理助手 / Doc Compliance Assistant

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `doc-compliance-assistant` v1.0.0 · LGD-Powered Security Family · Zero-dependency

**中文**：文档外发/提交前的一道本地闸门——归一化编码/BOM/换行/空白，同时扫出 PII（邮箱/手机号/身份证）、密钥（GitHub/AWS/OpenAI/私钥/URL 内嵌口令）、IP；命中即掩码报告，绝不打印明文。rc=0 干净 / rc=1 命中 / rc=2 用法错误。

**EN**: A local stop-gate before a document leaves your editor — normalize encoding/BOM/line-endings/whitespace, then scan in one pass for PII (email/CN-mobile/CN-ID), secrets (GitHub/AWS/OpenAI tokens, private keys, URL basic-auth), and IPs. Hits are masked, never printed. rc=0 clean / rc=1 findings / rc=2 usage.

## Usage / 用法
```bash
python scripts/doc_compliance.py --file path/to/draft.md
python scripts/doc_compliance.py --file path/to/draft.md --json
python scripts/doc_compliance.py --list-rules
```

## Disclaimer / 免责
Security aid only — regex scanners have false negatives; rc=0 means "no obvious patterns", not "safe". / 安全辅助，正则有误漏；rc=0 表示"未命中明显模式"，不等于"绝对安全"。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包代码 MIT
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

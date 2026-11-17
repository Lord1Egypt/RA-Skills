# AI 论断有证证据链（LGD-II 有证）· evidence-chain-builder

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> LGD-II evidenced · every act must carry evidence. Decompose claims into verifiable evidence chains — cure hallucination, strengthen proof.

## English

### Usage

```bash
python scripts/evidence_chain.py --claim "the defect rate of this product is below 0.5%" \
  --evidences "2025 QA report@official:company-QA" "no related customer complaints@internal:support"

python scripts/evidence_chain.py --from claim.json --json
```

Evidence format: `text@type:source`, where type is one of `official|paper|data|internal|assertion`. Verifiable types (official/paper/data) count with weight; the rest are down-weighted.

### Boundary (no fabrication)

This tool **does not judge whether a claim is true or false** — it only evaluates evidence quality. When verifiable evidence is missing, the claim is marked "do not conclude".

## 中文

> LGD-II 有证 · 凡所行必有证据。把论断拆成可验证证据链，治幻觉、强举证。

### 用法

```bash
python scripts/evidence_chain.py --claim "本产品不良率低于 0.5%" \
  --evidences "2025 质检报告@official:公司QA" "客户无相关投诉@internal:客服"

python scripts/evidence_chain.py --from claim.json --json
```

证据格式：`文本@类型:来源`，类型取 `official|paper|data|internal|assertion`。可验证类型（official/paper/data）计权，其余降权。

### 边界（不编造）

本工具**不判论断真假**，只评证据质量；缺可验证证据即标「勿作结论」。

© SynomosAI · MIT · LGD-Powered

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

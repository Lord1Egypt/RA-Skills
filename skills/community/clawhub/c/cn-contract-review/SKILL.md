---
name: CN Contract Review
description: "Review Chinese contracts for risky clauses — labor lease purchase NDA. Built-in 20+ rule sets."
metadata:
  category: Legal/Admin
  priority: P0
  languages: zh-CN
---

# Contract Review

Review Chinese contracts for risky clauses. Supports labor, lease, purchase, NDA, service agreements and more.

## Workflow

1. **Extract text** — read PDF/DOCX (python-docx / pdftotext / OCR fallback).
2. **Identify type** — classify contract type via keyword matching + AI:
   - 劳动合同, 租房合同, 购销合同, NDA, 服务协议, 借款合同, 担保合同, 股权协议, 装修合同, 合伙协议, 买卖合同, 承揽合同, 运输合同, 建设工程合同, etc.
3. **Load rule sets** — load 20+ built-in Chinese contract risk rule sets keyed by contract type.
4. **Scan clauses** — check each clause against rules:
   - 违约金比例 ≥ 30% → 🔴
   - 竞业限制期 > 2年 → 🔴
   - 保密期无限 → 🟡
   - 管辖权归属不利于乙方 → 🟡
   - 单方解约权 → 🟡
   - 空白授权条款 → 🔴
5. **Risk label** — assign severity per finding: 🔴 High / 🟡 Medium / 🟢 Low.
6. **Explain** — for each 🔴 finding, output:
   - Original clause excerpt
   - Plain Chinese explanation of the risk
   - Standard/recommended clause for comparison
7. **Summarize** — contract summary: parties, amounts, term, key dates, special conditions.
8. **Report** — structured report (JSON or Markdown) with summary, risk table, and recommendations.

## Sample Prompt

```
contract-review review --input 租赁合同.pdf
contract-review review --input 劳动合同.docx --type labor
contract-review review --input nda.pdf --type nda --severity-only high
contract-review batch ./contracts/*.pdf
contract-review rules --type labor  # list available rules
```

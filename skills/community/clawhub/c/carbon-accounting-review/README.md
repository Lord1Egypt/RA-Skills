# Carbon Accounting Review

Evidence-led review for GHG inventories, carbon disclosures and product-footprint methods.

**Author:** Simon Huang · **Version date:** 2026-11-12 · **Version:** 1.0.0.

**Format:** portable, text-only Agent Skill. **License:** MIT-0. The original release identifies its author; downstream attribution is appreciated but is not required by this license. No claim of endorsement by ISO, GHG Protocol, WRI, WBCSD or a regulator.

## What it does

- Reviews inventory boundaries, scope classification, source coverage and exclusions.
- Checks activity/factor units, provenance, GWP basis, allocation and double counting.
- Keeps location-based and market-based electricity separate.
- Reviews published emissions as reported assertions without inventing underlying calculation evidence.
- Screens PCF and carbon-software methods for traceability, comparability and verification gaps.
- Produces a bounded, actionable finding register rather than an unsupported compliance badge.

## Practical uses

| Scenario | Provide | Receive |
|---|---|---|
| Sustainability team preparing internal review | Selected inventory rows, boundary policy, factor references | Missing evidence, unit problems, Scope 2 treatment and follow-up checklist |
| Consultant reviewing a client's methodology | Authorized de-identified method note and data sample | Source-to-rule mapping, assumptions and limits for human review |
| Analyst checking a sustainability report | Selected report pages/tables and report year | Attributed claims, comparability cautions and not-assessable upstream evidence |
| Product team reviewing a PCF model | Functional/declared unit, lifecycle boundary, allocation and method references | Method gaps; not an ISO 14067 certificate or complete LCA |
| Developer validating carbon software requirements | Rules, synthetic records, test outputs | Implemented vs tested vs unverified coverage; no security-audit substitute |

## Try it

Install through your host's supported skill workflow after inspecting the files. ClawHub package identity and installation command will be shown on the published registry page; do not guess a publisher handle.

Start with the bundled [synthetic examples](examples/README.md), not live confidential data.

Example requests:

- “Review examples/inventory.json. Check units and Scope 2 treatment, and return findings with evidence locators. These factors are synthetic, not production data.”
- “Review these authorized report extracts. Keep reported totals separate from recalculated emissions and identify what cannot be assessed.”
- “Screen this product-footprint method. Check the declared unit, lifecycle boundary, allocation and comparability limits.”
- 「檢查這份去識別化碳盤查資料的單位、係數來源、Scope 2 雙重計算及缺漏證據，用繁體中文列出問題與補件清單。」

## Inputs and outputs

Inputs may be readable user-selected text, tables or files supported by the host. PDF/OCR/spreadsheet parsing is not supplied or guaranteed; disclose unreadable pages, extraction ambiguity and uninspected sheets. No API account or fixed external endpoint is required.

Output: [review template](templates/review-report.md) with scope, authorities/versions, evidence register, check status, calculations, limitations and prioritized next actions. Sample JSON is educational input, not a required production schema or machine-enforced validator.

## Requirements and data flow

The core skill needs a language-model host that supports Agent Skills. Optional document reading, public-source browsing and deterministic arithmetic use the host's existing authorized tools. No helper executable, auto-install step, environment variable or credential is included. Missing tools mean reduced, clearly labeled coverage—not permission to install or bypass restrictions.

The skill itself has no network client or telemetry. However, the host/model may send prompts and files to a provider. Check that environment's privacy policy and obtain required permission before providing confidential data. Public browsing, if separately authorized, must not include private values or document contents in queries. See [SECURITY.md](SECURITY.md).

## What it does not do

It does not supply emission factors, licensed standards, automatic arbitrary-PDF ingestion, a lifecycle database, filing/submission automation, legal advice, third-party assurance or certification. No emissions-reduction claim is established merely by a lower reported number. PCF review is method screening, not a comprehensive LCA or product-comparison service.

## Evidence and limitations

[Examples](examples/README.md) are deliberately small and synthetic. Their expected outcomes describe bounded checks, not representative accuracy, cross-model robustness or professional assurance. [Governance card](GOVERNANCE.md) states the declared data flow and risks. [Sources](references/sources.md) identify authorities to inspect; this package does not reproduce their standards. Review source editions for each real engagement.

## 中文摘要

這是一份給 AI 助理使用的「碳盤查審閱程序」，不是一鍵盤查系統。適合內部預審、顧問補件清單、公開碳揭露檢核及碳軟體方法審閱。強項是保留證據來源、找出重複計算與不可判定事項；正式查證、法規結論與重大決策仍需合格專業人員負責。

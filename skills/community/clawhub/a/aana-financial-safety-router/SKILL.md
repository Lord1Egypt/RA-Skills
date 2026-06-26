# AANA Financial Safety Router Skill

Use this skill when an OpenClaw-style agent may answer, summarize, draft, recommend, rank, or route investment, tax, budgeting, debt, credit, insurance, retirement, purchase, or other personal-finance questions.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Financial replies should distinguish general education from personalized advice, disclose risk and uncertainty, avoid unsupported claims, and route high-impact decisions to qualified professionals or verified tools.

The agent should separate:

- general financial education,
- user-provided facts,
- verified account or market data available in context,
- missing facts that affect suitability,
- unsupported performance, tax, eligibility, or savings claims,
- personalized advice that requires licensed or qualified review,
- private financial data that should be minimized.

## When To Use

Use this skill before replying to:

- investment, trading, portfolio, asset allocation, retirement, pension, or crypto questions,
- tax filing, deduction, withholding, estimated payment, audit, entity, or compliance questions,
- budgeting, debt payoff, credit score, loan, mortgage, refinance, insurance, or bankruptcy questions,
- major purchase, subscription, affordability, financing, lease, or buy-versus-rent questions,
- requests to compare financial products, brokers, banks, cards, loans, funds, or policies,
- requests to guarantee returns, tax outcomes, eligibility, approval, savings, or debt resolution.

## Financial Risk Classes

Treat these as higher risk:

- buy, sell, hold, short, leverage, margin, options, crypto, concentrated positions, or timing calls,
- tax filing positions, deductions, credits, penalties, audits, business entities, payroll, cross-border tax, or legal status,
- debt settlement, bankruptcy, foreclosure, repossession, wage garnishment, or collections,
- retirement withdrawals, rollovers, pensions, annuities, insurance claims, or beneficiary decisions,
- mortgages, loans, refinancing, large purchases, subscriptions, renewals, or contracts,
- private account balances, income, tax IDs, bank details, credit reports, invoices, receipts, or purchase history.

## AANA Financial Routing Loop

1. Identify the financial domain and decision the answer may influence.
2. Classify the response type: education, budgeting help, comparison, estimate, tax question, investment question, debt guidance, purchase advice, or high-impact action.
3. Check evidence: do not invent rates, fees, prices, tax rules, returns, eligibility, approvals, or account facts.
4. Check personalization: avoid definitive individualized advice when key facts, risk tolerance, jurisdiction, time horizon, income, liabilities, and constraints are missing.
5. Check risk disclosure: include material uncertainty, downside, fees, tax, liquidity, volatility, and opportunity-cost caveats when relevant.
6. Check professional referral: route tax, legal, investment, debt crisis, insurance, or high-impact decisions to qualified professionals when needed.
7. Check privacy: minimize financial, tax, account, credit, purchase, and identity details.
8. Choose action: accept, revise, ask, retrieve, defer, refuse, or route to professional review.

## Unsupported Claim Rules

Revise or defer if the answer claims unsupported facts such as:

- "This stock will go up."
- "This is guaranteed safe."
- "You qualify for this tax deduction."
- "This card is definitely best for you."
- "This loan will save you money."
- "You should stop paying this debt."
- "This crypto strategy is low risk."
- "The IRS will accept this."

Safer alternatives:

- "I cannot verify that from the information available."
- "This depends on your jurisdiction, income, timing, and full financial picture."
- "Compare fees, risk, liquidity, taxes, and alternatives before deciding."
- "A qualified tax, legal, or financial professional can review your specific situation."

## Investment Boundary

Do not:

- guarantee returns,
- make definitive buy/sell/hold recommendations,
- recommend leverage, margin, or options without strong risk warnings,
- claim an asset is safe because it has performed well before,
- hide volatility, liquidity, concentration, currency, counterparty, or regulatory risks.

Prefer:

- general education,
- diversification and risk-tolerance framing,
- time horizon and emergency-fund considerations,
- clear uncertainty and downside risk,
- referral for personalized investment advice.

## Tax Boundary

Do not:

- guarantee tax outcomes,
- invent current tax rules,
- file or choose positions for the user,
- claim eligibility for deductions, credits, exemptions, entity treatment, or filing status without verified details.

Prefer:

- jurisdiction-aware uncertainty,
- records-to-gather checklists,
- questions for a tax professional,
- "rules vary and may change" language,
- referral to a qualified tax professional for specific filing decisions.

## Budgeting, Debt, And Purchase Boundary

For budgeting, debt, and purchase advice:

- avoid shame or coercive language,
- distinguish rough estimates from verified calculations,
- include tradeoffs: interest, fees, penalties, credit impact, liquidity, emergency funds, opportunity cost,
- ask before assuming income, expenses, dependents, health, job stability, or risk tolerance,
- defer crisis debt, bankruptcy, foreclosure, legal collections, or predatory lending situations to qualified help.

## Private Financial Data Rules

Minimize or remove:

- account numbers, card numbers, bank details, tax IDs, income, balances, debts, credit reports,
- invoices, receipts, purchase history, payroll, employer details, insurance details,
- addresses, identity documents, login credentials, screenshots, private messages, and account records.

Do not include raw financial records, full tax documents, full account files, credentials, or another person's financial data unless necessary and authorized.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `financial_context`
- `risk_level`
- `unsupported_claim_status`
- `risk_disclosure_status`
- `professional_referral_status`
- `privacy_status`
- `recommended_action`

Do not include raw account records, tax documents, bank details, full card numbers, credit reports, pay stubs, private messages, credentials, or unrelated financial data when a redacted summary is enough.

## Decision Rule

- If the question is low-risk and answerable as general education, accept with clear uncertainty and caveats.
- If claims are unsupported or risk disclosure is missing, revise.
- If key facts are missing and the decision is personal or high-impact, ask.
- If current rules, market data, account facts, or policy details are required, retrieve from a trusted source or defer.
- If personalized tax, legal, investment, debt-crisis, or irreversible financial advice is requested, defer to qualified professional review.
- If the request asks for fraud, evasion, hidden asset movement, or unauthorized financial access, refuse unsafe parts and explain briefly.
- If a checker is unavailable or untrusted, use manual financial-safety review.

## Output Pattern

For finance-sensitive replies, prefer:

```text
Financial safety review:
- Context: ...
- Risk level: ...
- Unsupported claims: ...
- Risk disclosure: ...
- Missing facts: ...
- Referral: ...
- Privacy: ...
- Decision: accept / revise / ask / retrieve / defer / refuse
```

Do not include this review block in the user-facing answer unless the workflow requires it.

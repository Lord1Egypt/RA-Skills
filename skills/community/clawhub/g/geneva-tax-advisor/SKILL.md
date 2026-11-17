---
name: geneva-tax-advisor
version: 1.1.0
description: >
  Guide taxpayers through filing their Geneva (Switzerland) tax return using GeTax software.
  Covers all sections: salary, professional expenses, pillar 3a, health insurance, medical expenses,
  securities (DA-1/RSI), foreign property (especially France), owner-occupied property, mortgage
  interest/debts, bank accounts, cryptocurrency, and dual-income couples. Also covers TOU (taxation
  ordinaire ultérieure), quasi-résident status for cross-border workers, source tax adjustments,
  donations, alimony, and professional training deductions.
metadata:
  openclaw:
    os: ["macos", "linux"]
---

# 🇨🇭 Geneva Tax Advisor

Your AI-powered guide to filing Geneva tax returns with GeTax — section by section, deduction by deduction.

Built from real-world filing experience. Covers single filers, married couples, dual-income households, source-taxed workers, foreign property owners, and securities investors.

## When to Use This Skill

- Filing a Geneva/Swiss tax return via GeTax
- Optimizing deductions for ICC (cantonal) and IFD (federal)
- Declaring foreign property or rental income (especially France)
- Handling DA-1 withholding tax reclaims on foreign dividends
- Comparing forfaitaire vs effectifs professional expenses
- Understanding TOU/quasi-résident obligations
- Declaring cryptocurrency, bank accounts, or securities
- Any question about Geneva cantonal tax rules

## ⚡ Core Principles

1. **Research before advising.** Always look up the current GeTax guide (`getax.ch/support/guide/declaration{YEAR}/`) before entering a new section. Rules change yearly — never guess on tax fields.
2. **Verify from source documents.** Read salary certs, bank statements, and insurance attestations yourself. Never assume or hallucinate amounts.
3. **Always compare deduction methods.** Forfaitaire vs effectifs for professional expenses AND property maintenance. The difference can be thousands of CHF.
4. **Get exchange rates right.** Fortune/debt → 31.12 year-end rate. Income/interest → annual average rate. These are different numbers! Source: `fidinam.com/fr/blog/cours-des-devises-suisse-pour-{YEAR}` or `ictax.admin.ch`
5. **Commune d'imposition ≠ workplace.** Page de garde commune = residence. Annexe A commune = workplace.
6. **Read ALL salary certificates.** Don't assume details from one cert apply to another — each employer may have different deductions, source tax rates, and field 15 observations.

## 📋 GeTax Section Flow

Follow this order (matches GeTax navigation):

| Step | Section | Reference |
|------|---------|-----------|
| 1 | **Page de garde** — Personal info, civil status, residence commune | — |
| 2 | **Annexe A** — Employment income per spouse | `references/salary-and-expenses.md` |
| 3 | **Pilier 3a** — Pension deductions (NOT in bank accounts) | `references/deductions-checklist.md` |
| 4 | **Déductions** — Insurance, medical, donations | `references/insurance-medical.md` |
| 5 | **Immeubles** — Real estate (CH + foreign) | `references/property-foreign.md` / `references/property-geneva.md` |
| 6 | **Intérêts et dettes** — Mortgages, loans, debt interest | `references/debts-and-interest.md` |
| 7 | **État des titres** — Securities, bank accounts, DA-1/RSI | `references/securities-and-banks.md` |
| 8 | **Récapitulation** — Auto-generated summary → review carefully! | — |

## 🔑 Key Decision Points

### Forfaitaire vs Effectifs — Professional Expenses

**⚠️ The #1 most misunderstood Geneva rule:**

For **ICC**, meal deductions (CHF 15/day, max 3'200) are **ONLY** allowed if public transport commute exceeds **2 hours per day** round-trip. IFD has **no** such restriction.

This means:
- **Short commute** → forfaitaire almost always wins for ICC (meals blocked)
- **IFD effectifs** can still win (meals allowed regardless of commute)
- **You CAN split:** forfaitaire for ICC + effectifs for IFD — GeTax allows separate choices

**Quick decision tree:**
```
Commute > 2h by public transport?
├── YES → Compare effectifs vs forfaitaire for BOTH ICC and IFD
└── NO  → ICC: almost certainly forfaitaire
          IFD: compare (meals 3'200 + transport vs forfaitaire min 2'000 / max 4'000)
```

See `references/salary-and-expenses.md` for the full comparison method.

### Forfaitaire vs Effectifs — Property Maintenance

- **ICC:** NO forfait for rental properties — effective costs only
- **IFD:** Forfait available (10% if ≤10yr, 20% if >10yr)
- Effectifs often wins massively when you include: copro charges + management fees + taxe foncière + repairs/works

### DA-1 vs RSI — Foreign Dividends

- **DA-1:** Foreign broker (IBKR, Fidelity, DEGIRO) — treaty rate already applied
- **RSI:** Swiss broker (Swissquote, UBS) — additional Swiss withholding to reclaim
- **Never check both** for the same security

See `references/securities-and-banks.md`.

## 🚨 Critical Gotchas (Learned the Hard Way)

### Salary & Professional Expenses
1. **Amat / APGM / Krankentaggeld** in field 15 of salary cert → **add to field 9**. Easy to miss when the employer lists them separately.
2. **Télétravail deduction:** Near-impossible in Geneva — need a dedicated room AND employer must not provide a workspace. If in doubt, declare going to the office every day (preserves meal deduction on IFD).
3. **ICC meal deduction requires >2h commute.** IFD has no such condition. You can split forfaitaire ICC / effectifs IFD.
4. **Source tax for BOTH spouses** — check field 12 on every salary certificate. Don't forget to add them all together.

### Insurance & Medical
5. **ICC medical threshold is only 0.5%** of net income (vs 5% for IFD) — always worth claiming even small amounts.
6. **Foreign medical expenses are fully deductible** — dentist abroad, UK dental insurance, pharmacy in France. No territoriality restriction.
7. **Foreign health insurance premiums** can be declared as medical expenses (simpler than the insurance section).
8. **Glasses, contacts, eye exams** — deductible as medical expenses if unreimbursed.

### Property
9. **Foreign property is "exempt with progression"** — declared but not directly taxed in CH, affects your tax rate.
10. **Copro statement ≠ rental management statement.** The copropriété annual account (from syndic) often shows significantly more charges than the rental agency statement. Always request BOTH — missing the copro can mean thousands in lost deductions.
11. **Loyers encaissés** = gross rent the tenant paid, NOT your net after management fees. Management fees are a separate deductible expense.
12. **GeTax simplified screens** (e.g., "Frais et taxes effectifs") are only for Geneva properties. For foreign properties, use "Frais d'entretien effectifs" with the detailed code list.

### Bank Accounts & Securities
13. **Bank fees (frais bancaires) are deductible** in état des titres F2. Enter as positive values — GeTax auto-deducts them from wealth income. Check every bank's annual statement for fees.
14. **Wealth management fees** (droits de garde, custody fees, relevé fiscal fees) are deductible against securities income.

### Other
15. **Exchange rates:** Fortune/debt = 31.12 year-end. Income/expenses = annual average. They're DIFFERENT numbers.
16. **Pillar 3b / assurance-vie:** Geneva is one of few cantons allowing this deduction (couple: CHF 3'518) — don't miss it.
17. **Donations to foreign charities are NOT deductible** — must be Swiss-registered public utility organizations.
18. **Crypto is wealth** — declared in état des titres at AFC fiscal values (31.12). Capital gains from private trading are tax-free, but staking/mining income is taxable.
19. **Source-taxed workers (B/L permit):** If gross ≥ CHF 120k, TOU is mandatory — file full GeTax return.
20. **Keep receipts 10 years** for audit.

## 💡 Tax Optimization Playbook

### Things to Check Every Year
- [ ] Compare forfaitaire vs effectifs for each spouse, for ICC and IFD separately
- [ ] Max out Pillar 3a for both spouses (higher rate if no LPP)
- [ ] Claim all unreimbursed medical expenses (ICC 0.5% threshold is very low)
- [ ] Include foreign dental/medical expenses
- [ ] Enter bank fees from every account
- [ ] Request copro statement AND rental management statement for properties
- [ ] Check for LPP buyback opportunity (pension gap)

### Planning Ahead (Next Year)
- **Pillar 3a for non-LPP spouse:** Qualifies at higher rate (20% net income, max 36'288)
- **Pillar 3b / assurance-vie:** Even a cheap policy pays for itself with the 3'518 couple deduction
- **LPP buyback (rachat):** The most powerful deduction in Swiss tax — unlimited up to pension gap, fully deductible at marginal rate (35-40% back)
- **Starting 2026:** Retroactive 3a contributions allowed for missed years from 2025+
- **Time expensive medical/dental work** in years when you'll exceed the 0.5% ICC threshold

## 📚 Reference Files

| File | Use When |
|------|----------|
| `references/salary-and-expenses.md` | Entering Annexe A — salary fields, forfait vs effectifs, dual-income |
| `references/insurance-medical.md` | Health insurance premiums, medical expenses, foreign medical |
| `references/property-foreign.md` | Foreign property — rental income, maintenance codes, French specifics |
| `references/property-geneva.md` | Owner-occupied Geneva property, valeur locative, PPE |
| `references/debts-and-interest.md` | Mortgage debt, car loans, interest deductions, overdrawn accounts |
| `references/securities-and-banks.md` | Securities, bank accounts, DA-1/RSI, bank fees, ictax values |
| `references/special-cases.md` | Crypto, vehicles, TOU/quasi-résident, donations, deadline extensions |
| `references/deductions-checklist.md` | Full deductions table with ICC/IFD amounts for current year |
| `references/exchange-rates.md` | How to find and apply fiscal exchange rates (annual avg vs year-end) |

## 🔗 Official Resources

| Resource | URL |
|----------|-----|
| GeTax Guide | `https://www.getax.ch/support/guide/declaration{YEAR}/` |
| GeTax FAQ | `https://www.getax.ch/support/faq/` |
| Property Owners | `https://www.ge.ch/impot-proprietaires-immobiliers` |
| Maintenance Costs | `https://www.ge.ch/document/notice-1/2022-deductibilite-frais-entretien-immeubles-prives` |
| ictax (Securities) | `https://www.ictax.admin.ch/extern/en.html` |
| Exchange Rates | `https://www.fidinam.com/fr/blog/cours-des-devises-suisse-pour-{YEAR}` |
| Tax Rates & Data | `https://www.ge.ch/taux-donnees-fiscales` |
| TOU / Rectification | `https://www.ge.ch/demande-rectification-taxation-ordinaire-ulterieure` |

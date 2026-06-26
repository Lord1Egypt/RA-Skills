---
name: fibo-pensions
display_name: FIBO Pensions Module
source: EDM Council FIBO (Financial Industry Business Ontology)
url: https://spec.edmcouncil.org/fibo/
applies_to: Enterprise annuity, occupational annuity, pension management
validator: validators/fibo-mcp.md
---

# FIBO Pensions Seed Vocabulary

> Cold-start reference for enterprise annuity/pension domain wikis.
> Set `seed: fibo-pensions` in `meta.yaml` to reference this file.

## Basic Financial Concepts (FIBO-FND)

All financial domain wikis can reference:

| Standard Concept | Description | Usually Maps To in Wiki |
|-----------------|-------------|------------------------|
| LegalEntity | Organization with legal standing | Institution pages under entities/ |
| Contract | Contract/agreement | System pages under concepts/ |
| FinancialInstrument | Financial instrument | Product pages under entities/ |
| RegulatoryAgency | Regulatory agency | entities/ |
| Jurisdiction | Jurisdiction area | concepts/ |
| DatePeriod | Time period | Time fields in frontmatter |

## Business Entities (FIBO-BP)

| Standard Concept | Description | Common Confusion |
|-----------------|-------------|------------------|
| Organization | Organization | ≠ OrganizationalRole (organization ≠ organization role) |
| FunctionalEntity | Functional entity | e.g., "trustee" is a role, not the organization itself |
| Person | Natural person | |

## Securities (FIBO-SEC)

| Standard Concept | Description | Applicable Scenario |
|-----------------|-------------|---------------------|
| Fund | Fund | Public funds, enterprise annuity funds |
| Portfolio | Investment portfolio | ≠ Product (portfolio ≠ product) |
| Security | Security | |
| Issuer | Issuer | |

## Pensions-specific (FIBO-Pensions)

| Standard Concept | Chinese Mapping | Non-mixing Rule |
|-----------------|-----------------|-----------------|
| PensionPlan | Enterprise annuity plan | ≠ PensionFund (plan ≠ fund) |
| PensionFund | Enterprise annuity fund | ≠ PensionProduct (fund ≠ product) |
| PlanSponsor | Plan sponsor (enterprise) | |
| Trustee | Trustee | Is a role, not organization—same organization can be trustee and investment manager simultaneously |
| InvestmentManager | Investment manager | |
| Custodian | Custodian | |
| AccountManager | Account manager | |
| Beneficiary | Beneficiary (employee) | |
| VestingSchedule | Vesting schedule | |
| ContributionRate | Contribution rate | |
| DefinedBenefit | Defined Benefit (DB) | ≠ DefinedContribution (DC), China's enterprise annuity is DC type |
| DefinedContribution | Defined Contribution (DC) | |

## Relationship Templates

```
PlanSponsor --establishes--> PensionPlan
PensionPlan --managed_by--> Trustee (trustee management)
Trustee --delegates_to--> InvestmentManager (investment management)
Trustee --delegates_to--> Custodian (custody)
Trustee --delegates_to--> AccountManager (account management)
PensionFund --invests_in--> Portfolio
Beneficiary --participates_in--> PensionPlan
```

## Non-mixing Rules

| Easily Confused Concept Pair | Difference |
|------------------------------|------------|
| PensionPlan ≠ PensionFund | Plan is institutional arrangement, fund is money |
| PensionFund ≠ PensionProduct | Fund is capital pool, product is investment instrument |
| Organization ≠ FunctionalRole | A bank is organization, trustee is role; same organization can serve as trustee and account manager simultaneously |
| PlanType ≠ PortfolioCategory | Plan type (single/collective) ≠ Investment portfolio category (conservative/aggressive) |
| ContributionRate ≠ InvestmentReturn | Contribution rate ≠ Investment return rate |

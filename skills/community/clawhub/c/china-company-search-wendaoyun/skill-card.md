## Description:

Queries WenDaoYun APIs for Chinese company records, including basic company details, operating information, financial signals, public opinion, and risk indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rose-develop](https://clawhub.ai/user/rose-develop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to search for a Chinese company, confirm the intended company, and retrieve relevant WenDaoYun company records such as business status, legal risk, tax, customer, supplier, employment, and risk-index information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries legal, tax, risk, employment, customer, supplier, and person-linked company records that may be sensitive.

Mitigation: Review results before sharing them and limit disclosure to the intended business purpose.

Risk: The skill relies on a user-provided WenDaoYun API key.

Mitigation: Keep WENDAOYUN_API_KEY private, avoid including it in prompts or logs, and revoke it through WenDaoYun if it is exposed.

Risk: Company-name searches can return multiple similarly named organizations.

Mitigation: Confirm the specific company from search results before requesting detailed records.

## Reference(s):

- [WenDaoYun API Portal](https://open.wendaoyun.com/home)
- [WenDaoYun API Invoke Base URL](https://h5.wintaocloud.com/prod-api/api/invoke)
- [fuzzy-search-org - Company Fuzzy Search](references/fuzzy-search-org.md)
- [get-abnormal - Business Abnormality](references/get-abnormal.md)
- [get-bankruptcy-regroup - Bankruptcy Reorganization](references/get-bankruptcy-regroup.md)
- [get-bond-info - Bond Information](references/get-bond-info.md)
- [get-case-filing - Case Filing](references/get-case-filing.md)
- [get-cases-terminated - Terminated Enforcement Cases](references/get-cases-terminated.md)
- [get-clear-info - Liquidation Information](references/get-clear-info.md)
- [get-consumption-limits - Consumption Restrictions](references/get-consumption-limits.md)
- [get-customer - Customer Information](references/get-customer.md)
- [get-deliver-notice - Service Notices](references/get-deliver-notice.md)
- [get-dishonest-debtors - Dishonest Debtors](references/get-dishonest-debtors.md)
- [get-employment-detail - Employment Detail](references/get-employment-detail.md)
- [get-employment-info - Employment Information](references/get-employment-info.md)
- [get-environmental-penalties - Environmental Penalties](references/get-environmental-penalties.md)
- [get-equity-pledge - Equity Pledge](references/get-equity-pledge.md)
- [get-execute-info - Enforcement Information](references/get-execute-info.md)
- [get-exit-ban - Exit Restrictions](references/get-exit-ban.md)
- [get-gua-info - Guarantee Information](references/get-gua-info.md)
- [get-import-export-credit - Import and Export Credit](references/get-import-export-credit.md)
- [get-inq-eval - Inquiry Evaluation](references/get-inq-eval.md)
- [get-judicial-notice - Court Notices](references/get-judicial-notice.md)
- [get-judicial-sale - Judicial Sale](references/get-judicial-sale.md)
- [get-labour-arb - Labor Arbitration Delivery Report](references/get-labour-arb.md)
- [get-land-mortgage - Land Mortgage](references/get-land-mortgage.md)
- [get-open-court-arb - Labor Arbitration Hearing Notice](references/get-open-court-arb.md)
- [get-open-court - Court Hearing Notice](references/get-open-court.md)
- [get-pre-mediate - Pre-Litigation Mediation](references/get-pre-mediate.md)
- [get-public-inform - Public Notice](references/get-public-inform.md)
- [get-punishments - Administrative Penalties](references/get-punishments.md)
- [get-risk-index - Company Risk Index](references/get-risk-index.md)
- [get-risk - Company Risk Information](references/get-risk.md)
- [get-share-blocking - Equity Freeze](references/get-share-blocking.md)
- [get-simple-cancel - Simple Cancellation](references/get-simple-cancel.md)
- [get-supplier - Supplier Information](references/get-supplier.md)
- [get-tax-notice - Tax Arrears Notice](references/get-tax-notice.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries of selected company records with API request guidance when configuration is missing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided WENDAOYUN_API_KEY and user confirmation before detailed company lookups.]

## Skill Version(s):

1.2.31 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

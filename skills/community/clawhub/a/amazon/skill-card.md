## Description: <br>
Navigate Amazon as buyer, seller, or affiliate with price tracking, listing optimization, and smart purchasing decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to research Amazon products, compare deals, track prices, manage reorders, optimize seller listings, and prepare affiliate links with compliance reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with purchases or seller-account changes that affect money, shipping, or account state. <br>
Mitigation: Require explicit human approval before every purchase or seller-account change, and verify the total, shipping address, and payment method before proceeding. <br>
Risk: Amazon credentials, session cookies, payment details, or sensitive account data could be mishandled if provided to an agent. <br>
Mitigation: Do not provide passwords or raw cookies; avoid storing full payment details, passwords, tax IDs, or bank information, and use limited sessions or approved secrets storage where credentials are required. <br>
Risk: Automated shopping, scraping, affiliate, or seller workflows can violate platform, affiliate, or legal requirements when used without guardrails. <br>
Mitigation: Use official APIs where available, rate-limit requests, keep affiliate disclosures clear, and require manual confirmation for transactions and seller actions. <br>
Risk: Stored watchlists, price history, order summaries, or purchase preferences may expose sensitive consumer behavior over time. <br>
Mitigation: Keep retained shopping data limited to what the workflow needs and avoid sharing or selling purchase history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/amazon) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown with structured recommendations, comparison tables, checklists, and link or alert configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include purchase approval prompts, price-watch criteria, seller listing recommendations, affiliate disclosure reminders, and compliance cautions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

This skill helps review Taobao flash-sale product listings for prohibited goods, price fraud, misleading advertising, and related compliance risks, then returns a compliance rating and remediation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and compliance reviewers use this skill to pre-check Taobao flash-sale product listings before publication, investigate complaints, perform routine product compliance patrols, and identify price-compliance concerns. It is intended as a Chinese-language checklist and report generator, not as official legal advice or an automatic enforcement decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the generated compliance report as official legal advice or final enforcement authority.

Mitigation: Use the output as a checklist and route serious violations, delisting decisions, penalties, and customer-remedy decisions to qualified legal or compliance reviewers.

Risk: Taobao platform rules, advertising requirements, and product-category regulations may have changed after the skill's referenced sources.

Mitigation: Verify current Taobao rules, applicable law, and relevant regulator guidance before relying on recommendations.

Risk: The skill can flag that category credentials or price-history evidence are needed, but it cannot verify document authenticity or missing historical data by itself.

Mitigation: Confirm special-category licenses, cosmetic registration records, and price histories through authoritative business systems or official records.

Risk: The artifact presents an Alibaba internal-control role, but server evidence resolves the publisher as a third-party ClawHub user.

Mitigation: Verify any claimed Alibaba affiliation before using the skill in an Alibaba-controlled workflow or presenting the output as Alibaba-authored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/04-product-compliance)
- [Publisher profile](https://clawhub.ai/user/nic-yuan)
- [Taobao official rules center](https://rule.taobao.com)
- [GLOSSARY.md](docs/GLOSSARY.md)
- [INSUFFICIENCY-HANDLING.md](docs/INSUFFICIENCY-HANDLING.md)
- [RULE-UPDATE-SOP.md](docs/RULE-UPDATE-SOP.md)
- [LINKING-SOP.md Section 6B](docs/LINKING-SOP.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown compliance report with tables, ratings, risk lists, and remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language product compliance checklist output; no code execution, persistence, or hidden data access.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

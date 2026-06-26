## Description: <br>
Checks Taobao Flash Sale product listings for prohibited goods, advertising-claim risks, price-fraud signals, and description issues, then returns a compliance rating and remediation advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace compliance, operations, and merchant governance teams use this skill to pre-check product drafts, investigate complaints, run routine listing reviews, and assess price-promotion risks before making operational decisions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be mistaken for official Alibaba or platform guidance because the artifact uses an Alibaba internal-control framing. <br>
Mitigation: Treat the publisher as the third-party ClawHub handle nic-yuan and do not present the output as official Alibaba policy. <br>
Risk: Product takedowns, merchant penalties, refunds, and legal conclusions could be made from advisory output without current rule verification. <br>
Mitigation: Verify current Taobao rules and applicable law, and escalate serious or disputed cases to qualified legal or compliance reviewers before action. <br>
Risk: The skill cannot verify licenses, certificates, product evidence, image accuracy, or historical price records on its own. <br>
Mitigation: Require source documents, credential checks, listing screenshots, and price-history data before relying on high-risk findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/04-product-compliance) <br>
- [Taobao Rules Center](https://rule.taobao.com) <br>
- [GLOSSARY.md](docs/GLOSSARY.md) <br>
- [INSUFFICIENCY-HANDLING.md](docs/INSUFFICIENCY-HANDLING.md) <br>
- [RULE-UPDATE-SOP.md](docs/RULE-UPDATE-SOP.md) <br>
- [LINKING-SOP.md](docs/LINKING-SOP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown compliance report with ratings, risk tables, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Takes product listing details, complaint context, product batches, or price history as input; produces advisory compliance findings only.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

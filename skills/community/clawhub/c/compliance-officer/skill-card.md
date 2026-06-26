## Description: <br>
Reviews marketing content against FTC, HIPAA, GDPR, SEC 482, SEC Marketing, CCPA, COPPA, and CAN-SPAM using structured rule references with source URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arberx](https://clawhub.ai/user/arberx) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users, developers, and compliance reviewers use this skill to pre-review marketing copy, emails, landing pages, privacy policies, and draft disclosures against supported regulatory frameworks. The outputs are compliance guidance for human review, not final legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URL fetching may access private or access-controlled pages if the user supplies them. <br>
Mitigation: Only provide URLs intended for review and avoid private or access-controlled pages unless deliberate. <br>
Risk: Compliance findings or drafted disclosures could be mistaken for final legal advice. <br>
Mitigation: Use outputs as pre-review guidance and route final decisions through compliance or legal reviewers. <br>


## Reference(s): <br>
- [Agent Instructions](references/instructions.md) <br>
- [CAN-SPAM Rules](references/rules-can-spam.json) <br>
- [CCPA Rules](references/rules-ccpa.json) <br>
- [COPPA Rules](references/rules-coppa.json) <br>
- [FTC Claims Rules](references/rules-ftc-claims.json) <br>
- [FTC Dark Patterns Rules](references/rules-ftc-dark-patterns.json) <br>
- [FTC Endorsements Rules](references/rules-ftc-endorsements.json) <br>
- [GDPR Rules](references/rules-gdpr.json) <br>
- [HIPAA Rules](references/rules-hipaa.json) <br>
- [SEC 482 Rules](references/rules-sec-482.json) <br>
- [SEC Marketing Rules](references/rules-sec-marketing.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/arberx/compliance-officer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown compliance reviews, email reviews, privacy policy checklists, rule explanations, rule tables, and draft disclosure language with citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch user-provided URLs when network access is available; findings are pre-review guidance for human legal or compliance review.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

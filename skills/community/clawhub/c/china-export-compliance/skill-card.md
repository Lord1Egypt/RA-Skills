## Description: <br>
Helps AI agents assess China-focused export-control classification, license needs, technology-transfer limits, encryption export rules, and entity list screening for technology exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and compliance reviewers use this skill to triage whether software, AI models, encryption, or other technology exports from China may need classification, licensing, screening, or legal review. <br>

### Deployment Geography for Use: <br>
Global; focused on exports from China. <br>

## Known Risks and Mitigations: <br>
Risk: China export-control guidance can be jurisdiction-sensitive and may be incomplete for a specific product, origin, customer, or transaction. <br>
Mitigation: Confirm jurisdiction, export origin, product classification, and applicable legal regime before relying on it; consult qualified export-control counsel for production decisions. <br>
Risk: Security review noted unrelated third-party web-app promotion in the artifact. <br>
Mitigation: Do not send confidential compliance, product, customer, shipment, or legal data to unrelated external web apps linked by the skill. <br>
Risk: Broad legal-compliance triggers may invoke the skill outside its intended China export-control scope. <br>
Mitigation: Use it only for China-focused export-control triage and route unrelated compliance questions to better-scoped guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/china-export-compliance) <br>
- [Project homepage](https://github.com/lm203688/china-compliance-skills-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists, tables, and inline bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external tools or credentials are required; outputs should be reviewed by qualified export-control counsel before reliance.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

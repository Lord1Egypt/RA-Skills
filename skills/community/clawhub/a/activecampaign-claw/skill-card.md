## Description: <br>
ActiveCampaign agent for marketers + sales: list health, lead scoring, deliverability, campaign postmortems, automation diagnostics, and 40+ more reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ji282h7](https://clawhub.ai/user/ji282h7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing, sales, and operations users use this skill to analyze ActiveCampaign account health, campaign performance, automation behavior, contact quality, deliverability, and CRM pipeline activity from their own account data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ActiveCampaign API token may be able to modify important CRM or marketing records. <br>
Mitigation: Use a dedicated least-privileged ActiveCampaign integration user and set AC_READ_ONLY=1 when only reporting or analysis is needed. <br>
Risk: Some raw API examples or commands can bypass the skill's advertised write safeguards. <br>
Mitigation: Avoid running raw curl write examples, review every write request before execution, and prefer the audited script paths that enforce confirmations and write caps. <br>
Risk: Tokens and exported customer data can be exposed through command history, local files, or shared reports. <br>
Mitigation: Do not pass tokens directly on the command line, store local exports securely, prune reports when no longer needed, and limit access to the local user account. <br>


## Reference(s): <br>
- [ActiveCampaign Skill Page](https://clawhub.ai/ji282h7/activecampaign-claw) <br>
- [ActiveCampaign v3 API Reference](https://developers.activecampaign.com/reference) <br>
- [Contacts API Reference](references/contacts.md) <br>
- [Deals API Reference](references/deals.md) <br>
- [Custom Fields API Reference](references/custom-fields.md) <br>
- [Email Best Practices Framework](frameworks/email-best-practices.md) <br>
- [Segmentation Theory Framework](frameworks/segmentation-theory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, plain-English guidance, JSON or local files from supporting scripts, and shell commands for setup or analysis workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read live ActiveCampaign account data through the user's API token and may write local reports, exports, snapshots, history, and audit logs.] <br>

## Skill Version(s): <br>
1.9.4 (source: frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

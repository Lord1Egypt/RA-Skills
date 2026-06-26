## Description: <br>
Create CompleteTech LLC security, safety, permissions, and production-readiness review artifacts for agentic development workflows, including risk intake, tool permissions, secrets handling, data exposure, prompt-injection testing, retrieval trust, approval gates, external actions, audit logging, model/provider configuration, retention, dependency risk, least privilege, launch blockers, rollback, incident response, escalation, red-team results, and security signoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[completetech](https://clawhub.ai/user/completetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and delivery teams use this skill to select and draft practical security review artifacts for agentic workflows before launch, access expansion, configuration changes, or incident follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python rendering packages and create local Markdown, PDF, or PNG files. <br>
Mitigation: Review the declared packages before installation and write generated files only to approved local paths. <br>
Risk: Generated security-review artifacts are drafts and may contain placeholders or unverified project facts. <br>
Mitigation: Replace placeholders with verified workflow, data, tool, approval, logging, rollback, and incident-response details before relying on the output. <br>
Risk: Security-review outputs may include sensitive workflow, credential, or incident details. <br>
Mitigation: Store generated documents in access-controlled locations and review sharing permissions before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/completetech/agentic-security-review-skill) <br>
- [Project homepage](https://github.com/CompleteTech-LLC/agentic-security-review-skill) <br>
- [Security catalog](references/security-catalog.md) <br>
- [Security lifecycle](references/security-lifecycle.md) <br>
- [Security positioning](references/security-positioning.md) <br>
- [Use-case decision table](references/use-case-decision-table.md) <br>
- [Template index](references/template-index.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown drafts, branded PDF files, optional PNG previews, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts are drafts that require verified project facts before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

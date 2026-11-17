## Description:

AI-powered cross-border data compliance review agent that analyzes documents, matches regulations such as GDPR, CCPA, and PIPL, identifies risks, and generates actionable compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pillarscreation](https://clawhub.ai/user/pillarscreation)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, developers, SaaS startups, and compliance reviewers use this skill to review privacy policies, data processing agreements, and related documents for cross-border data compliance gaps. It supports document parsing, regulation matching, risk scoring, and bilingual report generation for global-market launch and vendor review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes handling sensitive uploaded documents and permanent storage of analysis history without clear retention controls.

Mitigation: Before production use, add clear user notices for document uploads, external processing, audit-log retention, record access, deletion, and export.

Risk: Compliance findings and recommendations may be incomplete, outdated, or unsuitable for a specific jurisdiction or business context.

Mitigation: Require review by qualified compliance or legal staff before relying on generated reports for launch, regulatory, or contractual decisions.

## Reference(s):

- [Datacomply Shield on ClawHub](https://clawhub.ai/pillarscreation/skills/datacomply-shield)
- [pillarscreation ClawHub profile](https://clawhub.ai/user/pillarscreation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with architecture notes, code snippets, shell commands, configuration examples, and report-output descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON, PDF, and Word compliance report outputs; generated reports should be reviewed by qualified compliance or legal staff.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

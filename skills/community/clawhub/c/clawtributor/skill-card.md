## Description:

Community incident reporting for AI agents. Contribute to collective security by reporting threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Security-focused agent users and maintainers use Clawtributor to draft, review, and sanitize incident reports about malicious prompts, vulnerable skills or plugins, and tampering attempts before manual submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing with an unpinned ClawHub installer can introduce supply-chain ambiguity.

Mitigation: Prefer a pinned or otherwise verified ClawHub installer before installing the skill.

Risk: Approved incident reports leave the local machine and may become visible to maintainers through the submission form.

Mitigation: Review and sanitize every report before approval, removing secrets, personal data, real conversations, and confidential information.

## Reference(s):

- [Clawtributor ClawHub listing](https://clawhub.ai/davida-ps/skills/clawtributor)
- [ClawSec homepage](https://clawsec.prompt.security)
- [Security Incident Report Form](https://github.com/prompt-security/clawsec/issues/new?template=security_incident_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON incident report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts reports locally and requires explicit user approval before any manual submission.]

## Skill Version(s):

0.0.6 (source: frontmatter, skill.json, changelog, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

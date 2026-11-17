## Description:

A2a Code Audit audits Python and JavaScript/TypeScript code for security vulnerabilities, style issues, and bugs and returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crftsmnd](https://clawhub.ai/user/crftsmnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to audit Python and JavaScript/TypeScript code for common security issues, style violations, and likely bugs before review or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted code may be sent to a paid external audit service.

Mitigation: Avoid confidential repositories or code containing secrets unless the publisher provides clear consent, payload, redaction, retention, and deletion terms.

Risk: The artifact describes local platform-only analysis, while server security evidence flags external-service behavior.

Mitigation: Review the skill behavior and pricing before installation or use.

## Reference(s):

- [ClawHub listing: A2a Code Audit](https://clawhub.ai/crftsmnd/skills/a2a-code-audit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with score, verdict, issue list, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity levels and PASS/WARN/FAIL verdict.]

## Skill Version(s):

1.0.2 (source: server release and skill.yaml, released 2026-04-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

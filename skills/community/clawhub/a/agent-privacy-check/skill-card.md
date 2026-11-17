## Description:

Audit an AI agent's reachable data, external data paths, and untrusted instructions, then explain the result in plain language with Low, Medium, High, or Critical severity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers, security reviewers, and agent operators use this skill to audit what an AI agent can access, where data can leave, and how untrusted instructions could influence tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect privacy-relevant configuration and filenames outside the intended scope.

Mitigation: Use the narrowest named scope, keep checks read-only, and avoid home directories, browser profiles, or service accounts unless explicitly intended.

Risk: A privacy audit can expose secrets if raw credential values, session contents, or private data are copied into the report.

Mitigation: Record secret types and locations only, redact values, and use synthetic data for examples or approved live tests.

Risk: Testing an external sink can send data to an unintended recipient.

Mitigation: Require explicit authorization before any network or upload test, use only an approved test endpoint with synthetic payloads, and otherwise mark the sink unverified.

## Reference(s):

- [Ward Agent Privacy Check](https://clawhub.ai/wardlu/skills/agent-privacy-check)
- [Evidence Collection](references/evidence-collection.md)
- [Platform Notes](references/platform-notes.md)
- [Risk Model](references/risk-model.md)
- [Report Template](references/report-template.md)
- [Source Notes](references/sources.md)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown privacy audit report with tables and ordered remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses evidence labels and redacts secrets; no raw secret values should be output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

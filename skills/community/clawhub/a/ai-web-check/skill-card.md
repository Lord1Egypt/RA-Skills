## Description:

Run an evidence-first, non-mutating AI website usability assessment for requests such as checking whether a site is agent-ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and website operators use this skill to run read-only checks that gather evidence about whether public website pages are findable, readable, understandable, navigable, and ready for AI-agent interaction. It helps identify candidate issues without certifying accessibility, security, vendor readiness, or successful business actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound GET requests may follow redirects to unexpected internal or third-party URLs.

Mitigation: Avoid scanning untrusted or attacker-controlled URLs from environments that can reach sensitive internal services until redirect and private-address validation are added.

Risk: Read-only scan results can be mistaken for certification of security, accessibility, AI vendor readiness, or completed business actions.

Mitigation: Treat PASS only as evidence for the named check, keep NOT_TESTED as unknown, and require independent evidence before making AIRead verified, accessibility, security, or action-completion claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/ai-web-check)
- [artifact/README.md](artifact/README.md)
- [artifact/profiles/README.md](artifact/profiles/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown or JSON reports, optionally written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use PASS, WARN, FAIL, NOT_APPLICABLE, and NOT_TESTED statuses and preserve evidence for named checks.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

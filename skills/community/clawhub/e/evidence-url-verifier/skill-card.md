## Description:

Verify evidence URLs are real and accessible. Check that artifact links resolve to actual content, not placeholders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and auditors use this skill to check that evidence URLs and local artifact paths are accessible, substantive, and aligned with the claimed content before completing or reviewing a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching untrusted evidence URLs can expose an agent to unsafe redirects, private network targets, or unexpectedly large downloads.

Mitigation: Use trusted URLs where possible, prefer HTTPS, block private and metadata IP ranges, validate redirects, and limit downloaded content size.

Risk: Evidence responses or URLs may contain sensitive information if logged verbatim.

Mitigation: Avoid logging full response contents and redact sensitive data in status reports.

Risk: Aggressive URL checking can create avoidable load on external services.

Mitigation: Respect rate limits such as the skill's documented maximum of one request per second.

## Reference(s):

- [Evidence URL Verifier on ClawHub](https://clawhub.ai/dalomeve/skills/evidence-url-verifier)
- [dalomeve publisher profile](https://clawhub.ai/user/dalomeve)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Analysis]

**Output Format:** [Markdown guidance with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URL status, content type, placeholder warnings, and local artifact existence checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

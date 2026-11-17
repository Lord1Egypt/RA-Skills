## Description:

Helps agents analyze API failures by using a four-role adversarial discussion pattern to diagnose issues, compare remedies, and converge on a recommended solution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot API call failures, compare candidate fixes, and produce a concise final recommendation for degraded or failing API integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debugging examples may cache model responses that contain API keys, request payloads, or other sensitive data.

Mitigation: Redact secrets and sensitive payloads before using the workflow, and review, delete, or secure any agent cache or debug output after troubleshooting.

Risk: The release is a workflow description rather than a complete runnable API-debugging engine.

Mitigation: Treat generated commands, code, and recommendations as implementation guidance, then review and test them in the target environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/auto-skill-20260404-063632)
- [Publisher profile](https://clawhub.ai/user/timo2026)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with diagnostic steps and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retry, fallback, network, and configuration checks for API debugging workflows.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

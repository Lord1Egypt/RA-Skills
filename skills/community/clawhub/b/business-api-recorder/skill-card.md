## Description:

Business API Recorder helps an agent record browser API traffic for an authorized web workflow and turn captured requests and responses into API documentation and reconstruction guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sihan2017](https://clawhub.ai/user/sihan2017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze authorized browser-based business workflows, capture their API call chains, and generate implementation documentation for understanding or rebuilding the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete browser API traffic logs can expose secrets, personal data, and confidential business payloads.

Mitigation: Use the skill only on systems you are authorized to monitor, prefer non-production or low-sensitivity accounts, and redact Authorization headers, cookies, tokens, personal data, and confidential payloads before sharing logs with an AI system or committing them to source control.

Risk: The documented installer pattern includes a curl-to-shell command.

Mitigation: Prefer verified installation steps and inspect installer content before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sihan2017/skills/business-api-recorder)
- [Skill Documentation](artifact/SKILL.md)
- [Implementation Document Template](artifact/DOCUMENT_TEMPLATE.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Chrome Extension Documentation](https://docs.openclaw.ai/tools/chrome-extension)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON API logs and Markdown implementation documentation, with supporting shell commands and browser-injected JavaScript.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captured logs may include request headers, cookies, tokens, personal data, and confidential payloads; review and redact logs before sharing or storing them.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

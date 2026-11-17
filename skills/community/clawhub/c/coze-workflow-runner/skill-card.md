## Description:

Runs Coze workflows through the Coze API to automate tasks such as content analysis, data processing, and image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjin714](https://clawhub.ai/user/hanjin714)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate to Coze, choose a workflow ID, pass input parameters, and process returned workflow content such as text, Markdown, JSON, or image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local Coze service credentials to invoke remote workflows.

Mitigation: Use a least-privilege Coze token and rotate or revoke it if the skill is no longer trusted.

Risk: The skill can run arbitrary Coze workflow IDs supplied by the caller.

Mitigation: Restrict execution to an approved allowlist of workflow IDs before installation or automated use.

Risk: Workflow inputs may contain sensitive personal or business data.

Mitigation: Send sensitive data only with user consent and after confirming the selected workflow is appropriate for that data.

Risk: Workflow outputs may include short URLs that are downloaded by following redirects.

Mitigation: Validate the host, redirects, file type, file size, and destination filename before downloading returned URLs.

## Reference(s):

- [Coze workflow list reference](references/workflows.md)
- [Coze workflow project reference](https://www.coze.cn/space/7555350866765545515/project-ide/7610360135081295918)
- [ClawHub skill page](https://clawhub.ai/hanjin714/skills/coze-workflow-runner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; workflow responses may include JSON, Markdown, text, or image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs remote Coze workflows and may return short URLs that require validation before download.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

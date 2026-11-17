## Description:

Automate Facebook Page posting and token management using Graph API with retry-safe, rate-limit-aware workflows for text and image content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunneetoichoi](https://clawhub.ai/user/yunneetoichoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Page operators use this skill to guide Facebook Page publishing workflows, including text posts, image posts, token exchange, environment setup, permission selection, and rate-limit-aware operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facebook Page access tokens, app IDs, and app secrets can expose publishing privileges if logged, committed, or shared.

Mitigation: Treat tokens and app secrets as sensitive, store them outside source control, and keep them out of logs and generated output.

Risk: Overbroad Meta app permissions can grant more Page access than the publishing workflow needs.

Mitigation: Limit permissions to the documented Page publishing use case and review Page access before deployment.

Risk: Separately supplied helper scripts are not part of this artifact and may introduce execution or data-handling behavior not covered by the package evidence.

Mitigation: Review and scan any helper scripts before running them with Page tokens or app credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunneetoichoi/skills/ai-agent)
- [Publisher profile](https://clawhub.ai/user/yunneetoichoi)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with API endpoint examples, environment variables, command-oriented workflow guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance only; no bundled executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

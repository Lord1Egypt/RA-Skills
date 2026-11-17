## Description:

Guides users through ClawdHub skill submission by diagnosing common publishing issues, checking basic skill structure, and explaining supported release paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahongting](https://clawhub.ai/user/mahongting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to troubleshoot ClawdHub submission failures, confirm required files, and choose an appropriate web, CLI, or import-based publishing path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a global latest CLI package or using an unverified package source can introduce supply-chain risk.

Mitigation: Verify the ClawdHub CLI package source and prefer pinned or isolated installs before following CLI examples.

Risk: Putting real tokens directly in shell commands or saved scripts can expose credentials.

Mitigation: Use interactive login flows, environment-specific secret handling, or a secrets manager instead of embedding real tokens.

## Reference(s):

- [Clawdhub Submit on ClawHub](https://clawhub.ai/mahongting/skills/clawdhub-submit)
- [ClawdHub documentation](https://docs.openclaw.ai/zh-CN/tools/clawhub)
- [ClawdHub project repository](https://github.com/clawd-hub/clawdhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, checklists, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; the skill does not automatically execute commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

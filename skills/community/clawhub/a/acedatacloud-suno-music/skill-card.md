## Description:

Guides agents in generating and editing music through AceDataCloud's Suno API, including lyrics, covers, stems, and multitrack projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to direct an agent to generate songs and lyrics, transform authorized audio, and manage music projects through AceDataCloud's Suno API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, audio URLs, and project data sent to the external service may contain sensitive material.

Mitigation: Review content and obtain rights to uploaded audio before submission; avoid sending sensitive material without approval.

Risk: Generation and custom-model operations may incur charges, and retries may repeat billable work.

Mitigation: Confirm costs and paid operations beforehand; check existing task status before retrying.

Risk: An exposed API token can allow unauthorized use of the service.

Mitigation: Use a scoped key where possible and keep it out of prompts and repositories.

Risk: Installing the optional MCP package introduces an additional software dependency.

Mitigation: Verify the package before choosing to install it.

## Reference(s):

- [Suno Music on ClawHub](https://clawhub.ai/acedatacloud/skills/suno)
- [AceDataCloud authentication guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud asynchronous task guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio links and task results depend on the external service; verify task completion before presenting them as final.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; bundled frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

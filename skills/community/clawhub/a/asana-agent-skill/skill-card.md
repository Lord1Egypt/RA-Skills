## Description:

Manage Asana tasks, projects, briefs, status updates, custom fields, dependencies, attachments, events, and timelines via Personal Access Token (PAT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[l-u-c-k-y](https://clawhub.ai/user/l-u-c-k-y)

### License/Terms of Use:


## Use Case:

Employees, external collaborators, and developers can use this skill to let an agent manage Asana task and project workflows through a PAT-backed CLI, including task discovery, updates, briefs, status updates, custom fields, dependencies, attachments, and timeline changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Asana PAT that can carry the same authority as the user's Asana account.

Mitigation: Use the least-privileged token available, store it through runtime configuration or environment injection, and avoid printing stored config values such as apiKey.

Risk: The skill can mutate live Asana data through create, update, comment, delete, follower, dependency, and timeline-shift commands.

Mitigation: Review generated commands before execution and test write paths in a non-production project first.

Risk: The upload-attachment command sends a local file path's contents to Asana.

Mitigation: Verify the file path and destination task or project before uploading.

Risk: Malformed rich text or unsupported tags can cause Asana API failures.

Mitigation: Use XML-valid HTML fragments wrapped in a body element and keep markup to Asana-supported tags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/l-u-c-k-y/skills/asana-agent-skill)
- [Asana Personal Access Token documentation](https://developers.asana.com/docs/personal-access-token)
- [Asana authentication documentation](https://developers.asana.com/docs/authentication)
- [Asana rich text documentation](https://developers.asana.com/docs/rich-text)
- [Asana attachment upload API reference](https://developers.asana.com/reference/createattachmentforobject)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw skills configuration documentation](https://docs.openclaw.ai/tools/skills-config)
- [Reference and implementation notes](references/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON from the CLI on stdout, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Asana PAT; command results are JSON-only.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manage Asana tasks, projects, briefs, status updates, custom fields, dependencies, attachments, events, and timelines via Personal Access Token (PAT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[l-u-c-k-y](https://clawhub.ai/user/l-u-c-k-y)

### License/Terms of Use:


## Use Case:

Developers, agents, and project teams use this skill to inspect and manage Asana workspaces through a PAT-backed CLI. It supports personal task triage and project-management workflows such as briefs, status updates, timelines, custom fields, dependencies, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived Asana PAT can authorize access to live workspace data.

Mitigation: Use the least-privileged or most limited PAT available, inject it only through the configured environment, and remove or rotate it when no longer needed.

Risk: Write, delete, upload, membership, and timeline-shift commands can change production Asana data.

Mitigation: Test write paths in a throwaway project first and require human review before deletes, uploads, membership changes, or timeline shifts.

Risk: Bulk timeline shifts can move many task dates without a built-in confirmation step.

Mitigation: Run timeline-shift commands with dry_run enabled first and review the proposed changes before applying them.

Risk: Stored API key values may expose the PAT if displayed or copied into prompts, logs, or shell history.

Mitigation: Avoid displaying stored apiKey values and keep tokens out of prompts, ad-hoc shell history, and logs.

## Reference(s):

- [Reference and implementation notes](references/REFERENCE.md)
- [Asana Personal Access Token](https://developers.asana.com/docs/personal-access-token)
- [Asana Authentication](https://developers.asana.com/docs/authentication)
- [Asana Rich Text](https://developers.asana.com/docs/rich-text)
- [Asana Attachment Upload API](https://developers.asana.com/reference/createattachmentforobject)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config)
- [OpenClaw Config CLI](https://docs.openclaw.ai/cli/config)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from CLI stdout, with Markdown setup and command guidance in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and an Asana PAT supplied through ASANA_PAT or ASANA_TOKEN.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

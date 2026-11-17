## Description:

Helps an agent read, summarize, create, update, and delete DingTalk Docs and DingTalk knowledge-base documents when a DingTalk document link or context is provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shyzhen](https://clawhub.ai/user/shyzhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw with DingTalk use this skill to locate, read, summarize, create, overwrite, modify, insert into, and delete DingTalk knowledge-base documents through DingTalk APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes high-impact document overwrite, block modification, and delete operations.

Mitigation: Require explicit user confirmation before overwrite or delete actions and review proposed content changes before execution.

Risk: The bundled whitelist configuration can allow broad workspace writes.

Mitigation: Replace the bundled whitelist with narrow, user-approved workspace and document targets before installation.

Risk: DingTalk app credentials and token access can affect remote documents outside the local workspace.

Mitigation: Install only with trusted DingTalk credentials, avoid low-level client commands, and remove or disable the get-token command where it is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shyzhen/skills/dingtalk-doc)
- [DingTalk knowledge-base overview](https://open.dingtalk.com/document/development/knowledge-base-overview)
- [DingTalk API Explorer](https://open-dev.dingtalk.com/apiExplorer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, configuration snippets, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DingTalk app credentials and a sender identity; write actions can modify or delete remote DingTalk documents.]

## Skill Version(s):

1.0.8 (source: server release evidence; artifact package.json reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

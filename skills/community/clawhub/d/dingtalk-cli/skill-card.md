## Description:

Helps agents use the local dingtalk-cli command to manage DingTalk knowledge bases, documents, workbooks, and document members through DingTalk Open Platform APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianen](https://clawhub.ai/user/ianen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure dingtalk-cli and run DingTalk document-management workflows, including reading and writing documents, querying knowledge-base nodes, reading .axls workbook ranges, and managing document members.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates sensitive workspace and document actions to an unpinned external CLI.

Mitigation: Install dingtalk-cli in an isolated environment, pin and review the package version, and use least-privilege DingTalk credentials.

Risk: Overwrite, delete, and member-change commands can modify or remove real DingTalk content or access.

Mitigation: Require explicit confirmation before executing overwrite, delete, or member-change commands, even when command examples include --yes.

## Reference(s):

- [DingTalk document node URL example](https://alidocs.dingtalk.com/i/nodes/xxx)
- [ClawHub skill page](https://clawhub.ai/ianen/skills/dingtalk-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Often recommends --json output for dingtalk-cli commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

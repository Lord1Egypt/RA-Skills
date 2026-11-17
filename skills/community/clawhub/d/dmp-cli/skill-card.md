## Description:

Use the Mingdata DMP CLI to manage audiences, insight tasks, media sync tasks, RTQ deals, and reference data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operations teams use this skill to configure and run the Mingdata DMP CLI for audience management, insight tasks, media sync, RTQ deal updates, and reference-data lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact DMP operations such as audience uploads, media syncs, and deal changes.

Mitigation: Confirm the intended DMP context, platform, advertiser, dataset, and authorization before running modifying commands.

Risk: The skill requires DMP credentials and upload secrets for non-interactive use.

Mitigation: Use least-privilege credentials from a secret manager or masked CI secrets, and avoid exposing secrets in prompts, logs, shell history, or command output.

Risk: The installation guidance downloads a CLI release before use.

Mitigation: Install a pinned, verified dmp release in a user-local path before execution instead of fetching an unreviewed latest binary during an agent task.

## Reference(s):

- [DMP CLI Command Reference](references/commands.md)
- [DMP CLI Workflows](references/workflows.md)
- [dmp-cli repository](https://github.com/a652/dmp-cli)
- [dmp-cli releases](https://github.com/a652/dmp-cli/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DMP CLI command sequences, environment-variable setup guidance, JSON parsing guidance, and operational checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

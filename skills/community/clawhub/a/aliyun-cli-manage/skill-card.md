## Description:

Use when users need command-line operations on Alibaba Cloud resources, including list, query, create, update, delete, credential and profile setup, region and endpoint selection, or API discovery from the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud resources through the official aliyun CLI, with guidance for installation, credential configuration, API discovery, bounded execution, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or replace the local aliyun executable before running cloud operations.

Mitigation: Prefer a manually verified Alibaba Cloud CLI installation, or review the downloaded package source and target install path before allowing the helper script to update the executable.

Risk: The skill operates on Alibaba Cloud resources using user credentials and can perform mutating actions.

Mitigation: Use least-privilege or short-lived credentials, confirm region and resource identifiers, run a minimal read-only query first, and validate one item in a small scope before batch or destructive operations.

Risk: Command outputs and saved logs may contain sensitive cloud resource details or credential-related errors.

Mitigation: Avoid placing access-key secrets in prompts or command arguments, prefer environment variables, and review saved output logs for sensitive data before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-cli-manage)
- [Sources](references/sources.md)
- [Alibaba Cloud CLI documentation hub](https://help.aliyun.com/zh/cli)
- [Install Alibaba Cloud CLI on Linux](https://help.aliyun.com/zh/cli/install-cli-on-linux)
- [Configure credentials for Alibaba Cloud CLI](https://help.aliyun.com/zh/cli/configure-credentials)
- [Alibaba Cloud OpenAPI Explorer](https://api.aliyun.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to save CLI version checks, API outputs, request parameters, result summaries, and error logs under output/aliyun-cli-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

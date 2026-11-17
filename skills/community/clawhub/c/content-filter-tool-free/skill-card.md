## Description:

内容过滤工具 helps individuals manage personal feed filtering with keyword, regular expression, author blocklist, whitelist, and local rule workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers use this skill to configure local feed filtering rules, block noisy authors or keywords, and review filtered content. It is intended for personal single-user feed cleanup rather than multi-account team rule synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill requests command and file authority and includes activation language for unrelated marketing and content-creation tasks.

Mitigation: Use the skill only for personal feed filtering and local rule management, and review the skill text before installation.

Risk: Suggested shell commands can affect local rule files or interact with feed service endpoints.

Mitigation: Inspect commands before execution, allow only expected filtering commands, and avoid passing untrusted user input directly into shell arguments.

Risk: Feed access tokens or API keys could be exposed if pasted into prompts, hard-coded in configuration, or saved in shared files.

Mitigation: Store tokens in environment variables, use least-privilege credentials, and confirm outputs do not include secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-filter-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local filtering rules, status summaries, debugging guidance, and command suggestions for feed filtering workflows.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

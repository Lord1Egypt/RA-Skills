## Description:

Helps customers prepare, submit, and manage Alibaba Cloud support tickets using the Workorder service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud customers and support teams use this skill to draft and manage after-sales support tickets, including viewing, replying to, closing, and rating cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read and modify support tickets using the authenticated aliyun CLI account.

Mitigation: Review each ticket preview and explicitly confirm writes one at a time; use an account with appropriate access.

Risk: The documented Linux CLI installation pipes a downloaded script to a shell.

Mitigation: Prefer a verified or package-manager installation of the CLI.

Risk: Version metadata differs between the ClawHub release and package files and may prevent live cloud operations.

Mitigation: Check the installed package's version compatibility before relying on ticket operations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-support)
- [Alibaba Cloud support](https://www.aliyun.com/service)
- [Workorder API reference](references/api-reference.md)
- [RAM policies](references/ram-policies.md)
- [Error handling contract](references/error-handling.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with ticket previews, status summaries, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ticket changes require an explicit preview and confirmation.]

## Skill Version(s):

0.0.2 (source: ClawHub release; packaged metadata reports 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

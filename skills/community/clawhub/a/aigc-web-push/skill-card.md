## Description:

Helps an AI agent create articles, image cards, and videos, then publish them to WeChat Official Accounts or websites through a cloud computer; it also supports content produced by other skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihengdao](https://clawhub.ai/user/lihengdao)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators use an AI assistant to draft articles, image cards, and videos, then prepare or publish that content to a configured WeChat Official Account or website through a cloud computer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a remote updater that can replace local files and unpinned install and update commands.

Mitigation: Review the update behavior and pin the release used for installation or updates; disable automatic updates if they do not fit the deployment.

Risk: The security review calls out external data sharing and draft-clearing capability as behaviors to assess before installation.

Mitigation: Review the data-sharing and draft-clearing behavior and confirm it is appropriate for the configured account before use.

Risk: The security review says four executable files were not fully inspected, leaving partial scan coverage.

Mitigation: Review the remaining executable code before relying on the skill in a sensitive environment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/lihengdao/skills/aigc-web-push)
- [Configuration wizard](https://design.pcloud.ac.cn/aigc-web-push.html)
- [虾评Skill listing](https://xiaping.coze.com/skill/015db5c8-8dc6-4c44-b16c-b865ea3c06f0)

## Skill Output:

**Output Type(s):** [Text, HTML, Rendered video files, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown, HTML, JSON, shell commands, and rendered video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create content files and publish them to a user-selected destination when requested; publishing requires user-provided account or cloud-computer configuration.]

## Skill Version(s):

3.4.4 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

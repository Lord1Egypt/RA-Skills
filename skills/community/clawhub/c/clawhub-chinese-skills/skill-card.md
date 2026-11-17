## Description:

从 ClawHub 最新上传的 skill 中筛选中文用户上传的 skill 并汇报给用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0nsense11](https://clawhub.ai/user/n0nsense11)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find recently uploaded Chinese-language skills on ClawHub and receive a concise list of matching skill links. It can also guide an optional daily report when the user requests ongoing monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional daily cron report could send results on an unintended schedule or to the wrong channel or account.

Mitigation: Confirm the cron schedule and delivery target before enabling the report, then review the created job and run one manual delivery test.

Risk: Results depend on the current ClawHub newest-skills page and may miss skills if the page fails to load or changes structure.

Mitigation: Retry page loading when needed and present an explicit no-results message if no Chinese-language skill is found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n0nsense11/skills/clawhub-chinese-skills)
- [ClawHub newest skills listing](https://clawhub.ai/skills?sort=newest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an optional cron schedule and delivery-check guidance when the user asks for recurring reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

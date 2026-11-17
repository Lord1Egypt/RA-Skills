## Description:

Automates Founder-HongYun academic publishing workflows, including journal editing tasks, DOI registration, review reminders, and WeChat article publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[behurry](https://clawhub.ai/user/behurry)

### License/Terms of Use:

MIT-0

## Use Case:

External journal editors and publishing operations staff use this skill to automate Founder-HongYun editorial workflows such as journal switching, overdue manuscript review, reviewer reminders, DOI registration, and WeChat article publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Founder-HongYun login/session credentials and WeChat publishing secrets.

Mitigation: Review before installing, use a trusted network and HTTPS Founder platform URL where possible, avoid logging raw cookies or WeChat secrets, and use least-privileged WeChat credentials.

Risk: The skill can perform high-impact publishing, DOI registration, and reviewer reminder actions.

Mitigation: Require manual preview and explicit final approval before any WeChat publication, DOI registration, or reviewer reminder is sent.

Risk: The server security summary reports insufficient confirmation or transport safeguards for some sensitive actions.

Mitigation: Deploy only where operators can audit browser network activity, confirm target records before execution, and stop workflows when the expected platform session or publication target is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/behurry/skills/founder-hy-editor-browser)
- [ClawHub publisher profile](https://clawhub.ai/user/behurry)
- [Founder-HongYun platform](http://journal.portal.founderss.cn/)
- [WeChat Official Accounts platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with inline commands, configuration values, and workflow status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response summaries, temporary session variable names, publication identifiers, DOI values, reviewer reminder results, and WeChat article URLs.]

## Skill Version(s):

0.1.9 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

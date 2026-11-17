## Description:

Express Tracker helps an agent identify courier carriers from tracking numbers or SMS text, query package status, maintain a local tracking list, and produce map links and daily delivery reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wumaoqianq](https://clawhub.ai/user/wumaoqianq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to track courier packages, parse forwarded delivery SMS messages, refresh package states, and generate concise delivery reports with route or tracking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers and the Juhe API key are sent to the primary courier endpoint over unencrypted HTTP.

Mitigation: Use only low-value test credentials until the endpoint is changed to HTTPS or the API provider documents a secure transport option.

Risk: The skill stores package numbers, courier status, trace history, and SMS-derived tracking data in a fixed local packages.json path.

Mitigation: Review the local data path before installation, restrict file access, and avoid forwarding SMS content that contains unrelated personal information.

Risk: The Juhe API key is read from a fixed desktop text file rather than a safer documented configuration mechanism.

Mitigation: Move credential handling to a documented secret store or environment configuration before using a valuable API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wumaoqianq/skills/express-hunter)
- [Juhe express API endpoint](http://v.juhe.cn/exp/index)
- [Kuaidi100 query endpoint](https://www.kuaidi100.com/query)
- [Amap route links](https://ditu.amap.com/dir)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON files, guidance]

**Output Format:** [Command-line text, Markdown-formatted status reports, URLs, and local JSON package records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local package state and uses courier API responses to produce tracking status, trace history, and map links.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

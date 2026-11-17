## Description:

计算八字以及大运流年信息，需要性别、ISO 8601 格式的时间两个参数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahaofan](https://clawhub.ai/user/ahaofan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can run this CLI skill to submit gender and ISO 8601 birth time data and receive Bazi chart, luck-cycle, and annual-cycle information from the 凡心八字 service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth details and optional name to a third-party service over unencrypted HTTP, so submitted data and returned results may be observed or modified on the network.

Mitigation: Review the data-sharing risk before installation or use; avoid submitting sensitive real names, use only trusted networks, and do not run the skill unless this exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahaofan/skills/bazi)
- [凡心八字官网](http://bagezi.top/)
- [凡心八字排盘 API endpoint](http://api.bagezi.top/api/paipan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, the requests package, gender, and an ISO 8601 birth time; name is optional and defaults to 张三.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Dingding helps agents send DingTalk group notifications as text, markdown, or link cards through a zero-dependency Python CLI, and provides concise DingTalk Open Platform development guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send CI/CD results, monitoring alerts, scheduled reports, and reminder messages to DingTalk groups. It is also useful for implementation guidance around common DingTalk Open Platform server APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can send markdown file contents to the URL provided through DING_WEBHOOK, so a misconfigured or malicious environment could transmit readable local text files outside the intended DingTalk endpoint.

Mitigation: Only run the skill in trusted environments, validate that DING_WEBHOOK targets https://oapi.dingtalk.com before sending, and require explicit confirmation before sending local file contents.

Risk: Using @all can create broad group notifications and operational noise.

Mitigation: Require user confirmation before using @all, and prefer targeted mobile-number mentions for alerts that need a specific responder.

## Reference(s):

- [DingTalk Open Platform](https://open.dingtalk.com)
- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/dingding)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI prints DingTalk API JSON responses and exits nonzero when DingTalk returns an error code.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

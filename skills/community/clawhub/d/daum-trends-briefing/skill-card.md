## Description:

Fetch Daum real-time trend TOP10, add one-line context (top news title) + links, and print a 12-line briefing suitable for OpenClaw cron + Telegram announce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkim](https://clawhub.ai/user/hunkim)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate short Daum real-time trend briefings for agent-run cron workflows and optional Telegram announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches live Daum trend and search pages, so automated announcements can reflect upstream page changes, transient fetch failures, or unsanitized web-derived text.

Mitigation: Review the output before relying on scheduled announcements, and add redirect limits, response-size limits, and output sanitization for automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunkim/skills/daum-trends-briefing)
- [Publisher profile](https://clawhub.ai/user/hunkim)
- [Daum homepage](https://www.daum.net/)
- [Daum search](https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS)
- [Example output screenshot](https://github.com/user-attachments/assets/9aefc56b-6f52-4580-b4e5-585bd0e816da)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text briefing and Markdown documentation with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script prints exactly 12 lines: a title, 10 trend entries, and an updatedAt line.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Check remaining CTExcel (UK) data, voice, and SMS allowances for an eSIM or physical SIM using the local ctexcel-usage CLI. Use when the user asks how much data is left, when a bundle expires, or wants a periodic balance summary. The CLI logs in with an SMS verification code and stores only the session cookie; this skill guides the code hand-off, interprets the JSON output, and explains what to do when the session expires.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baijian](https://clawhub.ai/user/baijian)

### License/Terms of Use:

MIT-0

## Use Case:

External users of CTExcel UK eSIMs or physical SIMs use this skill to check bundle allowances, expiry dates, and low remaining data. It guides SMS-based login when needed and presents the CLI results with the account masked.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Voice and SMS allowance reporting may be absent from the CLI results.

Mitigation: Check CTExcel's account page or contact CTExcel when voice or SMS usage matters.

Risk: Login uses an SMS verification code and a locally stored session cookie.

Mitigation: Request login details only when needed, keep codes and session data private, and follow the documented SMS cooldown.

## Reference(s):

- [CTExcel Usage Skill on ClawHub](https://clawhub.ai/baijian/skills/ctexcel-usage-skill)
- [CTExcel UK personal home](https://www.ctexcel.com/newcteuk)
- [API Notes](artifact/references/api.md)
- [Session Lifecycle](artifact/references/session.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Markdown]

**Output Format:** [Markdown guidance and allowance summaries based on JSON output, with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bundle name, expiry, resource totals and remaining amounts, remaining percentages, and a masked account identifier.]

## Skill Version(s):

0.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Search 3.2 billion leaked credentials in the COMB dataset via ProxyNova API (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibnaleem](https://clawhub.ai/user/ibnaleem)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners and developers use this skill to query ProxyNova's COMB dataset for authorized breach exposure checks by email, username, or password.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries containing emails, usernames, or passwords are sent to ProxyNova, a third-party leaked-credential API.

Mitigation: Use only identifiers you are authorized to investigate and avoid submitting live passwords, API keys, tokens, or other secrets.

Risk: Returned breach data can include sensitive credentials.

Mitigation: Redact returned credentials before sharing or storing results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ibnaleem/skills/comb)
- [ProxyNova COMB Tool](https://www.proxynova.com/tools/comb/)
- [Cybernews COMB Coverage](https://cybernews.com/news/largest-compilation-of-emails-and-passwords-leaked-free/)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required; ProxyNova returns up to 100 results per query and limits usage to about 100 requests per minute.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

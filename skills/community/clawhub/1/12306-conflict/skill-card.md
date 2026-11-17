## Description:

Provides utilities for logging in to the 12306 rail ticketing service and querying train tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiyang2007](https://clawhub.ai/user/feiyang2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate 12306 login setup and ticket-search workflows from Python while managing required account credentials and browser state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles 12306 credentials and can store session cookies in a predictable plaintext file.

Mitigation: Use a dedicated or low-risk 12306 account where possible, keep credentials and cookie files out of source control, restrict local file access, and delete 12306_cookies.json after use.

Risk: The release claims purchase automation while the reviewed evidence shows a gap between that claim and the login/query implementation.

Mitigation: Review the skill behavior before relying on purchase workflows and require human confirmation before any ticket purchase or account-impacting action.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/feiyang2007/skills/12306-conflict)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Python code, shell commands, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local 12306_cookies.json session-cookie file when login runs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

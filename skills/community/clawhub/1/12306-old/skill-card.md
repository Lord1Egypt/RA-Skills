## Description:

Provides Playwright-based tools for logging in to China Railway 12306, searching train tickets, and supporting ticket booking automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiyang2007](https://clawhub.ai/user/feiyang2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to automate 12306 account login and train-ticket lookup workflows. Because it can interact with real accounts and booking flows, users should review actions before allowing account or purchase-related activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may open a browser session for a real 12306 account and perform account or purchase-adjacent actions.

Mitigation: Require explicit user confirmation before login, booking, or purchase-related activity, and run only in a private workspace.

Risk: Session cookies can be saved in plaintext as 12306_cookies.json.

Mitigation: Avoid committing, sharing, or retaining generated cookie files, and delete them when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feiyang2007/skills/12306-old)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local browser session state and plaintext 12306_cookies.json when login automation is run.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

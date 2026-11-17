## Description:

Automates authorized data extraction and browser operations on Chinese domestic websites by connecting to a local logged-in Chrome session through CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[361066029](https://clawhub.ai/user/361066029)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate authorized data extraction or browser actions on Chinese sites that require an existing logged-in Chrome session, especially when generic browser automation is blocked at login or anti-bot gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over a logged-in Chrome session, including access to authenticated pages.

Mitigation: Use a separate Chrome profile, log in only to the target site, review target URLs and scripts before execution, and avoid sensitive accounts.

Risk: Scripts can execute page JavaScript against live authenticated sites and may perform state-changing actions if directed.

Mitigation: Limit use to explicitly authorized accounts and data, and review any action beyond read-only extraction before running it.

Risk: Automation against sites with anti-bot controls or account restrictions may violate terms when misused.

Mitigation: Respect site terms, robots guidance, and rate limits; handle verification manually and do not add CAPTCHA-solving automation.

## Reference(s):

- [Chrome setup and troubleshooting](references/setup.md)
- [Chinese site selectors and anti-bot notes](references/sites.md)
- [ClawHub skill page](https://clawhub.ai/361066029/skills/cn-browser-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; scripts may write JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on live website structure, logged-in session state, and user-provided target URLs or extraction JavaScript.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

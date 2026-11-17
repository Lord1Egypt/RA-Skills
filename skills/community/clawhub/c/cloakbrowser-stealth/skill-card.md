## Description:

CloakBrowser Stealth helps agents fetch and extract content from protected public pages when standard browser or fetch tools are blocked by anti-bot defenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve text, HTML, JSON, selected elements, or screenshots from non-login web pages that block ordinary fetch or browser automation. It is intended for authorized scraping and extraction workflows where anti-bot defenses otherwise prevent access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to bypass website anti-bot defenses and can be misused against sites where automation is not authorized.

Mitigation: Install and run it only for sites where automation is explicitly authorized, and do not use it to evade access controls or site policies.

Risk: Proxy-capable scraping and local browser execution can expose sensitive traffic, page contents, screenshots, or browser profile data.

Mitigation: Run the skill in an isolated environment with controlled network egress, avoid untrusted URLs, and clean up screenshots or browser profiles that may contain sensitive data.

## Reference(s):

- [CloakBrowser Configuration Reference](references/config.md)
- [ClawHub skill page](https://clawhub.ai/space-cadet/skills/cloakbrowser-stealth)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and script output as text, HTML, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch output is truncated by a configurable max character limit; screenshots may be written to a caller-provided local path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

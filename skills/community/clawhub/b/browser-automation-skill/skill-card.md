## Description:

Browser Automation helps agents control a real signed-in Chrome or Chromium browser through the published browser-relay-cli package and unpacked Browser Relay extension for tab, DOM, screenshot, and visible-content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasoncodespace](https://clawhub.ai/user/jasoncodespace)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to control a local, signed-in Chrome or Chromium session for page navigation, tab reuse, DOM-first actions, screenshots, visible-content inspection, and screenshot-guided fallback when selectors are unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad authenticated browser-control capability can expose sensitive browser state, personal data, or enterprise accounts to automation.

Mitigation: Use only with browser profiles and sites the user is comfortable exposing to automation, and avoid sensitive personal or enterprise accounts.

Risk: Floating npx usage can execute a changed remote browser-relay-cli package.

Mitigation: Prefer a pinned, reviewed browser-relay-cli version rather than floating npx commands.

Risk: The browser-control workflow could be misused for CAPTCHA bypass, stealth scraping, or anti-bot evasion.

Mitigation: Follow the documented safety rules and decline requests for CAPTCHA bypass, stealth automation, or anti-bot circumvention.

## Reference(s):

- [Browser Relay Commands](references/commands.md)
- [Browser Automation Skill Page](https://clawhub.ai/jasoncodespace/skills/browser-automation-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Browser Relay CLI commands that operate on a local signed-in Chrome or Chromium session.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

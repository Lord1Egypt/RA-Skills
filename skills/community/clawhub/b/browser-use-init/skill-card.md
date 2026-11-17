## Description:

Initializes Chrome DevTools Protocol mode for a real Chrome browser so agents can connect through Playwright or browser-use for web automation, data extraction, form filling, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzmeat](https://clawhub.ai/user/xyzmeat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to start Chrome with CDP enabled, inspect the connection, and connect either deterministic Playwright workflows or browser-use agents to an existing browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies a Chrome profile that may contain cookies, browsing history, bookmarks, and active login state.

Mitigation: Use a dedicated empty automation profile instead of a normal daily browsing profile, and avoid running the skill against sensitive accounts or sites.

Risk: The skill opens a CDP browser-control port, which can allow powerful control of the running browser session.

Mitigation: Keep the CDP port bound to local use, firewall it from other hosts, and close the Chrome session when automation is complete.

Risk: The launch script force-kills Chrome processes and starts Chrome through a shell command.

Mitigation: Review or patch start_chrome.py before deployment, especially the all-Chrome force kill behavior and shell-based launch path.

Risk: Browser-use agent tasks can act on pages through an LLM-controlled workflow.

Mitigation: Use constrained tasks, review outputs and side effects, and do not grant the browser session access to sensitive sites unless that risk is accepted.

## Reference(s):

- [Chrome CDP Solution](references/chrome-cdp-solution.md)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Playwright Chrome Connection Documentation](https://playwright.dev/python/docs/browsers#connect-to-an-existing-browser-instance)
- [browser-use Agent Documentation](https://docs.browser-use.com/)
- [Chrome App-Bound Encryption Background](https://developers.google.com/privacy-sandbox/3pcd)
- [ClawHub Skill Page](https://clawhub.ai/xyzmeat/skills/browser-use-init)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scripts for launching Chrome in CDP mode, querying the CDP endpoint, connecting Playwright, and running browser-use tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

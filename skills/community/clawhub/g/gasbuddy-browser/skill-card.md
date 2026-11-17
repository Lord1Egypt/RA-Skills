## Description:

Use Playwright via Bash `exec` tool (not the built-in browser tool) to fetch GasBuddy fuel prices for a target city/area (especially Toronto/North York), and return top station prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate GasBuddy city price checks and return the cheapest regular fuel stations with brand, price, and address details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks the agent to run local shell-driven Playwright automation.

Mitigation: Review the generated script before execution and run it only in a disposable or well-isolated environment.

Risk: The Playwright launch template disables Chromium sandboxing.

Mitigation: Prefer removing `--no-sandbox` and `--disable-setuid-sandbox` when the execution environment supports Chromium sandboxing.

Risk: Fuel prices and station data are live website content and may be incomplete if lazy loading or page challenges do not resolve.

Mitigation: Verify that enough station cards loaded and review the returned results before relying on the ranking.

## Reference(s):

- [GasBuddy North York gas prices](https://www.gasbuddy.com/gasprices/ontario/north-york)
- [GasBuddy Toronto gas prices](https://www.gasbuddy.com/gasprices/ontario/toronto)
- [ClawHub skill page](https://clawhub.ai/mebusw/skills/gasbuddy-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with JavaScript and shell-oriented execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a ranked list of fuel stations with brand, price, and address when the browsing workflow succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

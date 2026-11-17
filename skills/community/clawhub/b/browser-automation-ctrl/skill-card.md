## Description:

Controls a local headless Chrome browser through Selenium for navigation, element interaction, screenshots, page inspection, cookies, tabs, JavaScript execution, proxy settings, and user-agent changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tr0812](https://clawhub.ai/user/tr0812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows in a local headless Chrome session, including opening pages, interacting with elements, collecting page data, managing tabs and cookies, and saving screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation can visit pages, interact with elements, execute JavaScript, and change cookies beyond a narrow task scope.

Mitigation: Run only after review in an isolated browser environment and limit use to sites and sessions the agent is explicitly allowed to access.

Risk: Screenshots and page exports may capture private or sensitive page content.

Mitigation: Avoid sensitive or logged-in websites unless that access is intended, and review saved files under ~/Pictures/OpenClaw before sharing them.

Risk: Proxy, user-agent, cookie commands, and disabled Chrome sandboxing reduce browser isolation and can change how web sessions are routed or identified.

Mitigation: Use a disposable profile or sandboxed host, and review proxy, user-agent, and cookie commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tr0812/skills/browser-automation-ctrl)
- [Artifact skill documentation](artifact/SKILL.md)
- [Browser control script](artifact/scripts/browser_ctrl.py)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime commands return JSON and may save PNG or PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are saved under ~/Pictures/OpenClaw when file output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

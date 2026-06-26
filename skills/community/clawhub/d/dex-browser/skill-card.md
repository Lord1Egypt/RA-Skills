## Description: <br>
Dexter Browser Automation provides Playwright-based browser automation for JavaScript-rendered pages, UI interaction, structured extraction, and screenshots when simpler web tools are insufficient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylerdotai](https://clawhub.ai/user/tylerdotai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as a last-resort browser layer when pages require JavaScript rendering, UI interaction, screenshots, or structured extraction that static fetch tools cannot provide. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad live-browser automation can interact with websites and accounts in ways that may be unauthorized or inappropriate. <br>
Mitigation: Use only on sites and accounts where access is authorized, supervise actions, and prefer search or static fetch tools before browser automation. <br>
Risk: Credentials, private page content, screenshots, or downloads can be exposed through command arguments or generated files. <br>
Mitigation: Avoid passing real passwords on command lines, keep screenshots and downloads in safe temporary or workspace paths, and review outputs before sharing. <br>
Risk: The JavaScript evaluation path can run arbitrary code in the browser context. <br>
Mitigation: Review JavaScript before running cdp.py eval and restrict it to trusted pages and necessary tasks. <br>
Risk: Anti-bot or stealth-oriented automation guidance can be misused to bypass site controls or policies. <br>
Mitigation: Do not use the skill to evade access controls, rate limits, terms of service, or other site restrictions. <br>


## Reference(s): <br>
- [CSS Selectors Reference](references/selectors.md) <br>
- [Common Browser Automation Patterns](references/patterns.md) <br>
- [ClawHub release page](https://clawhub.ai/tylerdotai/dex-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; invoked scripts return JSON and may write screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Playwright and Chromium; rendered HTML is truncated to 50000 characters, extracted items are capped at 50, and screenshots default to /tmp/screenshot.png unless a path is provided.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

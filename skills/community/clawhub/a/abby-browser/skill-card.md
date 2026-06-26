## Description: <br>
Abby Browser helps an agent control OpenClaw browser actions such as opening pages, taking screenshots, clicking elements, typing into forms, extracting page text, waiting, and scrolling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earnabitmore365](https://clawhub.ai/user/earnabitmore365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent perform supervised browser tasks through OpenClaw, including navigation, screenshots, element interaction, form entry, and page content extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can click elements, type text, submit forms, and otherwise act in a real browser session. <br>
Mitigation: Supervise use on logged-in or sensitive sites and require confirmation before high-impact browser actions. <br>
Risk: The extraction helper can evaluate JavaScript built from CSS selector input. <br>
Mitigation: Use trusted selectors only and review extraction requests before execution. <br>
Risk: Screenshots and extracted page text may include sensitive page content. <br>
Mitigation: Review what pages are open before capture or extraction and handle generated files and text as potentially sensitive. <br>


## Reference(s): <br>
- [Abby Browser ClawHub release](https://clawhub.ai/earnabitmore365/abby-browser) <br>
- [OpenClaw Browser Docs](https://docs.openclaw.ai/cli/browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown or text responses with OpenClaw browser command examples, action results, extracted page text, and screenshot file references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser actions operate in the user's active browser environment and may produce local screenshot files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

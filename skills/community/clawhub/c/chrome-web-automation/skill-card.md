## Description: <br>
Automates an existing Chrome session to inspect tabs, click, fill forms, capture screenshots, and debug web flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive a live Chrome session for web app debugging, form filling, screenshot capture, and reproducing UI issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may view or operate sensitive content in active Chrome tabs. <br>
Mitigation: Close sensitive tabs or use a separate browser profile, and specify the exact site or tab the agent should use. <br>
Risk: Browser automation can perform sensitive actions such as submitting forms, purchases, posts, deletions, or account changes. <br>
Mitigation: Require explicit approval before any sensitive browser action is submitted or confirmed. <br>
Risk: Page changes can make element references stale and cause actions to target the wrong page state. <br>
Mitigation: Re-snapshot after navigation or large DOM updates before continuing interaction. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown notes with screenshot or evidence artifacts when captured] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser interaction transcripts, screenshots, and reproduction notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

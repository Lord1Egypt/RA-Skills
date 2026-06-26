## Description: <br>
Uses Playwriter to control a user's logged-in Chrome browser and ask AI assistants such as Gemini for expert advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13801201404-sys](https://clawhub.ai/user/13801201404-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill when an AI website requires an already logged-in browser session. It provides Playwriter steps for opening Chrome, creating a session, navigating to a target site, submitting a question, and retrieving the response text or a screenshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation against logged-in AI websites can expose personal or work account context. <br>
Mitigation: Use a dedicated browser profile or low-risk account, avoid sensitive data, and clean up sessions and screenshots after use. <br>
Risk: The security scan notes risky support for bot-detection bypass and under-scoped browser automation. <br>
Mitigation: Review carefully before installing, verify the Playwriter package and extension, and do not use the skill to bypass anti-bot controls or site rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13801201404-sys/ask-expert-playwriter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and Playwriter JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser response text or screenshots through Playwriter commands; no fixed output schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Automate browser actions locally via browser-use CLI/Python: open pages, click/type, screenshot, extract HTML/links, debug sessions, and capture login QR codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengjiajie](https://clawhub.ai/user/fengjiajie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate local browser workflows with browser-use, including page inspection, screenshots, DOM or HTML extraction, QR code capture, and OpenAI-compatible LLM agent runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local browser automation can capture sensitive page content in screenshots, HTML dumps, QR crops, and persistent sessions. <br>
Mitigation: Use only authorized pages, scope API keys and LLM endpoints, and delete screenshots, HTML dumps, QR crops, and sessions when finished. <br>
Risk: LLM-driven browser tasks can send page context or task details to an external OpenAI-compatible endpoint. <br>
Mitigation: Use trusted endpoints and avoid private or logged-in pages unless that data flow is authorized. <br>


## Reference(s): <br>
- [Browser Use Local on ClawHub](https://clawhub.ai/fengjiajie/browser-use-local) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local creation of screenshots, HTML dumps, QR crops, and browser session artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Build and run Gemini 2.5 Computer Use browser-control agents with Playwright, including a screenshot -> function_call -> action -> function_response loop and safety confirmation for risky UI actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[am-will](https://clawhub.ai/user/am-will) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation builders use this skill to run Gemini 2.5 Computer Use browser-control loops with Playwright, including screenshot-driven model actions and user confirmation for actions that require safety review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser screenshots, page URLs, and prompts are sent to a third-party Gemini model during operation. <br>
Mitigation: Use a sandboxed browser profile and avoid logged-in or sensitive sites unless that exposure is intentional. <br>
Risk: Model-driven browser automation may take unwanted UI actions. <br>
Mitigation: Keep turn limits low, use --exclude to block actions that should not be automated, and require confirmation for safety-sensitive actions. <br>


## Reference(s): <br>
- [Gemini Computer Use Notes](references/google-computer-use.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with bash commands and a Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY; browser screenshots, page URLs, and prompts are sent to Gemini during operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

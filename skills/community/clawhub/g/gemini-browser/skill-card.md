## Description: <br>
Query Google Gemini via browser automation using OpenClaw's Browser Relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eccstartup](https://clawhub.ai/user/eccstartup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to ask Google Gemini questions from a manually attached Chrome tab and extract Gemini responses through OpenClaw Browser Relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a real, logged-in Chrome tab and can access content visible in the attached Gemini session. <br>
Mitigation: Attach only the intended Gemini tab and prefer a dedicated Chrome profile or non-primary Google account. <br>
Risk: Clipboard extraction can expose unrelated sensitive clipboard contents. <br>
Mitigation: Use DOM extraction when the clipboard may contain sensitive data, or clear and verify the clipboard before reading it. <br>
Risk: Browser Relay uses page-context JavaScript evaluation to interact with Gemini's editor. <br>
Mitigation: Keep execution limited to the documented Gemini DOM operations and review commands before running them. <br>


## Reference(s): <br>
- [Gemini Browser on ClawHub](https://clawhub.ai/eccstartup/gemini-browser) <br>
- [Google Gemini](https://gemini.google.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and extracted response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a manually attached Chrome tab, OpenClaw Browser Relay, and an authenticated Google Gemini session.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

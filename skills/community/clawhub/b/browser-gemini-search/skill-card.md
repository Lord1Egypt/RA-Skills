## Description: <br>
Use Google Gemini (gemini.google.com) to search the web via OpenClaw's browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream007007s](https://clawhub.ai/user/dream007007s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an OpenClaw agent to open or focus Gemini in their Chrome session, submit a search query, and report Gemini's response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls the user's existing Chrome session for Gemini, which can expose open tabs or account state to browser automation. <br>
Mitigation: Run it only when Gemini browser automation is intended, prefer a separate Chrome profile, and close sensitive tabs before use. <br>
Risk: Chrome must run with remote debugging enabled, increasing the importance of profile and local-machine access hygiene. <br>
Mitigation: Enable remote debugging only for the session where the skill is needed and approve browser-profile access deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dream007007s/browser-gemini-search) <br>
- [Google Gemini](https://gemini.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown with browser-control steps and inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chrome remote debugging on port 9222 and an approved user browser profile.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

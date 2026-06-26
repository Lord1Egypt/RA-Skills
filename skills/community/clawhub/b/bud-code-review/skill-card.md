## Description: <br>
AI-powered code review using Gemini that reviews entire projects, catches bugs, suggests fixes, and helps debug. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Python and other code with Google Gemini, identify bugs, security issues, performance problems, and request suggested fixes or debugging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed code or file contents can be sent to Google Gemini. <br>
Mitigation: Use the skill only with code you are permitted to share with Google Gemini, and avoid repositories or files that may contain secrets or confidential data. <br>
Risk: The script contains an embedded fallback Gemini API key. <br>
Mitigation: Patch or audit the script before sensitive use and require users to provide their own GEMINI_API_KEY. <br>
Risk: AI-generated review findings and fixes may be incomplete or incorrect. <br>
Mitigation: Treat results as review assistance, then validate findings, tests, and code changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stigg86/bud-code-review) <br>
- [Google AI Studio](https://aistudio.google.com) <br>
- [Gemini generateContent endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown-style text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized findings, suggested fixes, debugging guidance, and overall assessment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

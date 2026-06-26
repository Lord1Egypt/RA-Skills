## Description: <br>
Generates code and images through Claude AI and Gemini web interfaces when official APIs are not configured or available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metiu1](https://clawhub.ai/user/metiu1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to route code generation, code analysis, and image generation requests through provider web interfaces when official APIs are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request Claude, Google, or Gemini login credentials and attempt to store account secrets. <br>
Mitigation: Do not provide raw passwords to the agent; log in directly through the provider website or use official API/OAuth flows. <br>
Risk: The skill may send private code, proprietary prompts, personal data, or generated files to third-party services. <br>
Mitigation: Confirm the content is appropriate to share before allowing submission to external web services. <br>
Risk: The skill depends on web sessions, provider availability, and CAPTCHA flows that may interrupt automation. <br>
Mitigation: Expect manual intervention for login, CAPTCHA, or inaccessible services, and use official APIs when available. <br>


## Reference(s): <br>
- [Claude AI](https://claude.ai) <br>
- [Gemini](https://gemini.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown, code blocks, shell commands, or generated image files depending on the request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require interactive login, CAPTCHA handling, and user confirmation before sending private content to third-party services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

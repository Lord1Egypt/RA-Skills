## Description: <br>
ALAPI integration assistant that helps developers search ALAPI endpoints, read documentation, extract parameters, generate integration code, and make confirmed token-based ALAPI calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anhao](https://clawhub.ai/user/anhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find ALAPI endpoints, understand parameters and response shapes, generate minimal integration code, and perform live ALAPI tests only when a token and explicit confirmation are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated ALAPI calls may use an ALAPI token from the local environment instead of only a freshly supplied token. <br>
Mitigation: Review before installing when ALAPI_TOKEN is set locally, prefer explicit confirmation before authenticated network calls, and avoid exposing the raw token in prompts, commands, logs, or final responses. <br>
Risk: Generated integration code could place ALAPI credentials in client-side applications or hard-coded source. <br>
Mitigation: Keep ALAPI_TOKEN in server-side environment or configuration, use a backend proxy for frontend projects, and use placeholders rather than real token values in generated code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anhao/alapi) <br>
- [ALAPI base API](https://v3.alapi.cn) <br>
- [ALAPI documentation pattern](https://www.alapi.cn/api/{id}/introduction) <br>
- [Code examples](references/code-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, JSON, Guidance, API Calls] <br>
**Output Format:** [Markdown with code blocks, JSON summaries, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live ALAPI responses only after explicit user request and token availability; should not echo raw tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

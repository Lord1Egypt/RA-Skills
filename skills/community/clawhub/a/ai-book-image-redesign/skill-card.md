## Description: <br>
将用户提供的单文件 HTML 或前端原型封装为可复用的静态网页应用 skill，并提供本地初始化和静态站导出脚本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn an existing HTML/front-end image redesign prototype into a local static web app, then export deployable files for Vercel or another static host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The static browser app stores API endpoint settings and API keys in browser localStorage. <br>
Mitigation: Use trusted endpoints, prefer short-lived or low-privilege keys, and clear browser storage or modify the page to avoid saving keys. <br>
Risk: Uploaded manuscript images and credentials can be sent to user-entered remote endpoints. <br>
Mitigation: Avoid confidential manuscript images unless the selected provider is approved, and prefer a backend proxy with environment-injected credentials for production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kelcey2023/ai-book-image-redesign) <br>
- [Publisher Profile](https://clawhub.ai/user/kelcey2023) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands plus generated static HTML and JSON deployment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a browser-based static image redesign tool that accepts user-provided API endpoint, API key, model name, prompt, and uploaded images.] <br>

## Skill Version(s): <br>
1.0.100 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

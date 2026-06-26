## Description: <br>
让AI代理控制浏览器自动化网页操作。支持 Claude/GPT/Gemini/Ollama，可执行填表、购物、搜索等任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill as a browser-use guide for installing, configuring, and applying AI-controlled browser automation to form filling, shopping, search, comparison, and account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents that can control live browsers, including logged-in accounts, cloud browser sessions, shopping, email, and form submission. <br>
Mitigation: Use a dedicated browser profile, avoid syncing primary account sessions to cloud browser environments, and require manual approval before purchases, messages, uploads, applications, or other account-changing actions. <br>
Risk: The skill includes a remote shell script for syncing browser profile information. <br>
Mitigation: Inspect remote shell scripts before execution and run them only in an environment where browser credentials and API keys are intentionally scoped for automation. <br>
Risk: The skill requires sensitive credentials for Browser Use Cloud and optional LLM providers. <br>
Mitigation: Store API keys in local environment configuration, restrict their permissions where supported, and rotate keys if they are exposed to shared browser or agent sessions. <br>


## Reference(s): <br>
- [browser-use GitHub repository](https://github.com/browser-use/browser-use) <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/browser-use-guide) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API key configuration, browser-use CLI commands, Python examples, OpenClaw integration notes, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

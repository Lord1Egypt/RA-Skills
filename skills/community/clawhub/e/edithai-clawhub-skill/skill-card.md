## Description: <br>
Intelligent log analysis CLI tool powered by DeepSeek API with 30+ built-in tools for file operations, system diagnostics, and log pattern recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xin9min9](https://clawhub.ai/user/xin9min9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use Edithai to inspect text, JSON, CSV, application, and system logs with natural-language queries, interactive analysis, and generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs, generated reports, API keys, and conversation history may contain sensitive data. <br>
Mitigation: Redact secrets and personal data before analysis, keep API keys out of source control, and clear ~/.edithai/history.json after sensitive sessions. <br>
Risk: The skill depends on an external npm package and sends relevant log content to the DeepSeek API. <br>
Mitigation: Install only if the package is trusted and the deployment is allowed to send the analyzed content to DeepSeek; use a dedicated, quota-limited API key. <br>
Risk: File access and diagnostic command execution can expose or modify local system context if configured too broadly. <br>
Mitigation: Run the tool from a limited directory and configure command allowlists and blacklists for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xin9min9/edithai-clawhub-skill) <br>
- [README](artifact/README.md) <br>
- [Capabilities](artifact/CAPABILITIES.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Quick reference](artifact/QUICK-REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language analysis, Markdown-style reports, structured JSON responses, file exports, and inline shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DEEPSEEK_API_KEY, supports interactive sessions, and may store conversation history in ~/.edithai/history.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Prompt injection detection and security scanning for OpenClaw agents. Installs the ai-sentinel plugin via OpenClaw CLI, configures plugin settings, and offers local (Community) or remote (Pro) classification with dashboard reporting. All configuration changes require explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amandiwakar](https://clawhub.ai/user/amandiwakar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add AI Sentinel protection to an OpenClaw project, choose local or Pro scanning behavior, configure plugin settings, and verify that prompt-injection detection is working. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit OpenClaw configuration and local environment files. <br>
Mitigation: Review the exact target path and proposed diff before approving changes, and prefer project-local configuration unless global settings are intended. <br>
Risk: Pro mode can transmit scan results or message content to api.zetro.ai. <br>
Mitigation: Use Community mode for local-only scanning, or enable Pro only for code and prompts you are allowed to share. <br>
Risk: Incorrect plugin settings may block benign traffic or fail to enforce prompt-injection protections. <br>
Mitigation: Start in monitor mode, choose an appropriate confidence threshold, restart OpenClaw, and run the verification steps before relying on enforcement. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/amandiwakar/ai-sentinel) <br>
- [Zetro AI](https://zetro.ai) <br>
- [AI Sentinel npm package](https://www.npmjs.com/package/ai-sentinel) <br>
- [AI Sentinel dashboard](https://app.zetro.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose OpenClaw configuration changes and Pro-tier environment variable setup after user confirmation.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

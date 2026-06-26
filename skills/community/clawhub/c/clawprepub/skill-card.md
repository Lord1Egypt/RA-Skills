## Description: <br>
Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins, for an OpenClaw environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinjianfenghzau-wq](https://clawhub.ai/user/qinjianfenghzau-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and prepare the `ai-assistant-security-openclaw` plugin, generate a login authorization link, and complete basic local configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer fingerprints the device and binds the machine to a remote ClawSentry account. <br>
Mitigation: Install only when the publisher is trusted and remote account binding is expected; review the login endpoints before execution. <br>
Risk: The bundled installer changes local OpenClaw plugin configuration and restarts the OpenClaw gateway. <br>
Mitigation: Review the bundled script and run it in an environment where OpenClaw configuration changes and gateway restart are acceptable. <br>
Risk: Local `.state` files and logs may contain login or API-key-related data. <br>
Mitigation: Protect the `.state` directory during use and delete retained logs or state files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinjianfenghzau-wq/clawprepub) <br>
- [Volcengine support site](https://www.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and login URL instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a login URL and instruct the agent to relay post-login verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

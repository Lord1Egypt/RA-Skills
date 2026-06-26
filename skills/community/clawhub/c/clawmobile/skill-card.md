## Description: <br>
ClawMobile helps agents operate Android automation workflows through AutoX.js, including workflow management, task recording, AI-assisted recovery, membership-gated features, and HTTP API interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miyan1221](https://clawhub.ai/user/miyan1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, test engineers, and automation operators use this skill to control Android devices, run or record workflows, validate connectivity, and generate automation guidance for mobile testing and RPA tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remotely control an Android device. <br>
Mitigation: Install and run it only for intended Android automation use cases, and review each workflow before execution. <br>
Risk: Weak default authentication and broad network binding can expose device-control APIs. <br>
Mitigation: Replace default tokens, bind services to localhost or a trusted network, and avoid public API exposure. <br>
Risk: Recording and automation may capture screenshots, UI trees, logs, task files, or API responses from sensitive apps. <br>
Mitigation: Avoid recording or automating sensitive apps unless data storage and retention locations are understood and controlled. <br>
Risk: Persisting real tokens in shell startup files can leak credentials. <br>
Mitigation: Use a secret manager or scoped runtime environment variables instead of storing production tokens in ~/.bashrc. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/miyan1221/clawmobile) <br>
- [ClawMobile Documentation](https://docs.clawmobile.com) <br>
- [AutoX.js Documentation](https://autoxjs.com/) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AutoX.js API requests, Android automation workflow parameters, setup steps, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
ClawGuard Security Checker v3 analyzes OpenClaw security configuration, runtime integrity, permissions, and hardening recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stardreaming](https://clawhub.ai/user/stardreaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to assess OpenClaw configuration security, identify risky settings, and generate hardening guidance before applying configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect sensitive local configuration, environment, log, or optional memory data. <br>
Mitigation: Run it against a specific OpenClaw configuration path, avoid broad secret, log, and memory scans unless explicitly needed, and confirm user consent for sensitive-file inspection. <br>
Risk: Generated hardening changes can alter authentication, network binding, sandbox, or command execution behavior. <br>
Mitigation: Back up the existing configuration, review the generated hardened JSON, and apply changes in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stardreaming/clawguard-checker) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report text with optional JSON report files and hardened configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a hardened OpenClaw configuration file when used with --fix.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Comprehensive guide for installing, configuring, operating, and troubleshooting OpenClaw, a self-hosted, multi-channel AI agent gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bengii](https://clawhub.ai/user/bengii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to install, configure, operate, secure, and troubleshoot self-hosted OpenClaw gateways across messaging channels, model providers, agents, nodes, and local tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide administrative actions such as installs, restarts, configuration changes, elevated execution, local shell commands, node device actions, and remote workflow runs. <br>
Mitigation: Require explicit operator confirmation before following any suggested administrative or execution step. <br>
Risk: The skill covers sensitive paths involving tokens, session directories, PDFs, memory, Firecrawl, and cloud embedding providers. <br>
Mitigation: Review proposed actions for secret exposure and data movement before sharing values, changing files, or enabling integrations. <br>
Risk: The security evidence marks the release suspicious because broad OpenClaw administrator guidance is not consistently paired with strong guardrails. <br>
Mitigation: Install only when detailed OpenClaw administrator guidance is needed, and review the skill and scan results before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bengii/bengii-gemini-fix) <br>
- [Publisher Profile](https://clawhub.ai/user/bengii) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw Install Documentation](https://docs.openclaw.ai/install) <br>
- [OpenClaw Architecture Documentation](https://docs.openclaw.ai/concepts/architecture) <br>
- [Security Reference](artifact/references/security.md) <br>
- [Gateway Operations Reference](artifact/references/gateway_ops.md) <br>
- [Configuration Reference](artifact/references/config_reference.md) <br>
- [Exec Tool Reference](artifact/references/exec.md) <br>
- [Secrets Reference](artifact/references/secrets.md) <br>
- [Sandboxing Reference](artifact/references/sandboxing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local administration steps that require operator review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Install and configure the ClawGuard security plugin - an LLM-as-a-Judge guardrail that detects and blocks risky tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidan-capsule](https://clawhub.ai/user/lidan-capsule) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, and troubleshoot ClawGuard for OpenClaw gateways so risky tool calls can be evaluated and optionally blocked before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawGuard can inspect and log tool-call JSON, which may expose sensitive tool context in gateway logs. <br>
Mitigation: In sensitive environments, disable full tool-call logging where appropriate and review log retention and access controls before deployment. <br>
Risk: Security evaluation sends tool-call context to the configured LLM provider. <br>
Mitigation: Confirm which provider receives evaluation context and use a local or approved model when policy requires it. <br>
Risk: Gateway tokens may be exposed during troubleshooting commands. <br>
Mitigation: Redact gateway tokens from copied logs, tickets, and shared terminal output. <br>


## Reference(s): <br>
- [ClawGuard ClawHub Page](https://clawhub.ai/lidan-capsule/clawguard) <br>
- [ClawGuard GitHub Repository](https://github.com/capsulesecurity/clawguard) <br>
- [ClawGuard npm Package](https://www.npmjs.com/package/@capsulesecurity/clawguard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands, configuration tables, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes plugin installation steps, OpenClaw configuration options, Docker commands, verification checks, and troubleshooting notes.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

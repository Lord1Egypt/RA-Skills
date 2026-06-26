## Description: <br>
Advanced prompt injection defense with multi-layer protection, memory integrity, and tool security wrapper. OWASP LLM Top 10 2026 compliant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill as a front-line guardrail for autonomous agents, validating user input, memory/context loads, tool calls, and outputs before normal agent logic proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill acts as a front-line policy gate and can block agent execution. <br>
Mitigation: Install it only where this blocking posture is desired, configure highest priority deliberately, and test expected workflows for false positives before relying on it. <br>
Risk: The skill reads declared memory and identity files and writes persistent local security logs. <br>
Mitigation: Review the listed workspace paths before deployment and monitor local audit and incident logs for sensitive operational details. <br>
Risk: Telegram or webhook alerts can disclose security event metadata to configured destinations. <br>
Mitigation: Use only trusted alert destinations and keep webhook alerts disabled unless external monitoring is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/anti-injection-skill) <br>
- [Project homepage](https://github.com/georges91560/anti-injection-skill) <br>
- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command snippets, plus runtime allow/block decisions and local log entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires highest-priority execution, declared workspace file access, and optional operator-configured alert destinations.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

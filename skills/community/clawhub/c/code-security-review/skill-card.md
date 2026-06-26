## Description: <br>
Guides an agent to perform practical security reviews of code and systems, focusing on real risks such as injection, XSS, path traversal, insecure deserialization, authentication and authorization flaws, key leaks, insecure logging, and command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they ask an agent for a security review, code audit, vulnerability analysis, or security assessment. It structures findings by severity, impact, remediation, and patch guidance while discouraging fabricated issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to inspect source code and suggest patches during a review. <br>
Mitigation: Install and run it only in repositories where that level of code access and patch proposal is acceptable. <br>
Risk: Security findings can be incomplete or incorrect if the reviewed context is partial. <br>
Mitigation: Review findings before acting on them and provide the agent with relevant code paths, configuration, and trust-boundary context. <br>


## Reference(s): <br>
- [Common Vulnerability Checklist](artifact/references/checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/code-security-review) <br>
- [Publisher Profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown findings with severity labels, remediation steps, and optional code diffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are limited to substantiated risks; clean reviews should briefly confirm no risks found.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

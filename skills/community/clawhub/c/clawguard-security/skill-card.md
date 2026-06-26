## Description: <br>
AI Agent Immune System - Security scanner, PII sanitizer, and intent-action mismatch detector with 285+ patterns, OWASP Agentic AI Top 10 coverage, and local-only operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeuZhou](https://clawhub.ai/user/NeuZhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run local security scans, sanitize possible PII before sharing text with external services, and compare intended actions against potentially dangerous commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells agents to run an unpinned external npm command automatically across broad situations. <br>
Mitigation: Prefer manual scans, pin and verify the CLI package before use, and require explicit user control for recurring or background scans. <br>
Risk: The sanitizer may process sensitive text or real secrets before the CLI source and data handling are fully audited. <br>
Mitigation: Do not run sanitizer commands on real secrets until the CLI implementation and local data handling have been reviewed. <br>


## Reference(s): <br>
- [ClawGuard homepage](https://github.com/NeuZhou/clawguard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, analysis] <br>
**Output Format:** [Markdown with inline bash code blocks and concise scan or warning summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill invokes Node-based CLI commands through npx and may produce text, JSON, or SARIF scan output depending on command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

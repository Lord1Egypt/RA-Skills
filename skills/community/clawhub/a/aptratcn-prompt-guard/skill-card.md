## Description: <br>
Detect and block prompt injection attempts in inputs by identifying suspicious patterns, preventing malicious instructions, and ensuring secure AI interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Prompt Guard to review untrusted user input, web content, file content, and API responses for prompt-injection indicators before an agent acts on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the skill as a technical security boundary rather than advisory policy guidance. <br>
Mitigation: Keep normal sandboxing, tool approvals, and least-privilege controls enabled when using the skill. <br>
Risk: Logging suspected prompt-injection attempts can capture sensitive user or system data. <br>
Mitigation: Avoid storing sensitive data in logs and redact suspicious input before retention or sharing. <br>


## Reference(s): <br>
- [Prompt Guard ClawHub release](https://clawhub.ai/aptratcn/aptratcn-prompt-guard) <br>
- [README.md](artifact/README.md) <br>
- [ATTACK_PATTERNS.md](artifact/ATTACK_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with detection checks, response templates, and setup snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory guardrail guidance; no runtime dependencies are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

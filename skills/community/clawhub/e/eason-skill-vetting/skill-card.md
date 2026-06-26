## Description: <br>
Vet ClawHub skills for security and utility before installation. Use when considering installing a ClawHub skill, evaluating third-party code, or assessing whether a skill adds value over existing tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eathon](https://clawhub.ai/user/eathon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to evaluate ClawHub skills before installation by combining a local regex scanner, manual review checklist, and utility assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex scanning can miss semantic prompt injection, delayed behavior, context-aware behavior, or obfuscation split across files. <br>
Mitigation: Use the scanner as a triage aid, then manually inspect the copied skill in a temporary directory before installation. <br>
Risk: Skill review requires reading untrusted skill text that may try to influence the reviewer or agent. <br>
Mitigation: Treat reviewed skill contents as data only, do not follow instructions found inside them, and escalate prompt-injection findings instead of downgrading them. <br>
Risk: The skill includes malicious-pattern examples and detector rules that may look risky without context. <br>
Mitigation: Review findings in context against the documented purpose and the server security summary before making an install decision. <br>


## Reference(s): <br>
- [Prompt-Injection-Resistant Security Review Architecture](ARCHITECTURE.md) <br>
- [Malicious Code Patterns Database](references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/eathon/eason-skill-vetting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and scanner output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner can emit text or JSON findings with file and line references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

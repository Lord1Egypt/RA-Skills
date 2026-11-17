## Description:

AnyGen图表生成器 helps agents use the AnyGen CLI and the www.anygen.io rendering service to turn text descriptions into flowcharts, architecture diagrams, sequence diagrams, mind maps, and related visual diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, product teams, and automation users can use this skill to generate diagram assets from structured natural-language descriptions for documentation, architecture review, process analysis, and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram prompts and callback URLs may be sent to or interact with AnyGen's external service.

Mitigation: Do not submit confidential diagram content, callback endpoints, or internal system details unless organizational policy allows that service use.

Risk: API keys can be exposed when pasted directly into shell commands or logs.

Mitigation: Prefer environment-based credential handling and avoid committing, logging, or sharing real AnyGen API keys.

Risk: The skill depends on an additional AnyGen workflow skill for generation orchestration.

Mitigation: Review the dependent skill before installation and accept it only when its behavior matches the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/anygen-diagram-free)
- [AnyGen service](https://www.anygen.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated diagram links or local file paths depending on AnyGen service output and account permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

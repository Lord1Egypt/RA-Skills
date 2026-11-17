## Description:

Gunakan saat user meminta reasoning mendalam bertahap, self-correction, atau output anti-repetitif terverifikasi pada tugas nyata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use Aurum Brain as a meta reasoning and self-check layer for tasks that need structured analysis, self-correction, verified output, and reduced repetition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local reasoning logger can persist sensitive task text if users pass secrets, private prompts, regulated data, or credentials to it.

Mitigation: Redact sensitive text before using scripts/reasoning_log.py and avoid passing API keys, passwords, private prompts, regulated data, or other secrets to the logger.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/aurum-brain)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with optional inline shell commands for the local reasoning logger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional logger writes local JSONL records and should not receive secrets or sensitive text.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

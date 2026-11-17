## Description:

Automatically learns from an agent's subagent work and turns repeated complex tasks into reusable draft skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to detect recurring subagent tasks, generate draft skills from eligible completions, and manage draft promotion or archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript summaries may be converted into draft or active skill instructions without enough review.

Mitigation: Keep summaries non-sensitive and require human review of generated SKILL.md content and lifecycle metadata before promotion or use.

Risk: Workspace path defaults may write generated skills outside the intended location.

Mitigation: Set AUTO_SKILL_WORKSPACE explicitly and install only in workspaces where automatic skill creation is acceptable.

Risk: Generated active skills can contain low-quality or unsafe instructions.

Mitigation: Treat produced skills as untrusted until they have been reviewed and scanned before deployment.

## Reference(s):

- [Auto Skill Extractor on ClawHub](https://clawhub.ai/wahajahmed010/skills/auto-skill-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts emit JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create draft SKILL.md files and lifecycle metadata in the configured workspace.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

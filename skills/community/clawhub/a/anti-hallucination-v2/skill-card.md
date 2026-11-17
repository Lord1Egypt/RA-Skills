## Description:

Anti-Hallucination provides behavioral verification workflows that help AI agents reduce fabrication by checking facts, code, files, and outputs before responding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianmao1989](https://clawhub.ai/user/qianmao1989)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external users can use this skill to add structured fact-checking, code verification, source labeling, and post-output review workflows to accuracy-sensitive agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage broad file inspection, web searching, URL access, and code execution.

Mitigation: Require explicit user approval and task-specific scope before running code, browsing arbitrary URLs, searching broadly, or using filesystem and shell tools.

Risk: Persistent installation of the rules can change agent behavior beyond the immediate task.

Mitigation: Review the rules before adding them to persistent agent instruction files and disable automatic execution in environments with shell, filesystem, or network tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianmao1989/skills/anti-hallucination-v2)
- [Repository listed in artifact metadata](https://github.com/CherryAI/anti-hallucination)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline command examples and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes strict, balanced, and fast verification modes with confidence and source-labeling conventions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

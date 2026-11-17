## Description:

12Agent Novel coordinates a Chinese long-form novel writing workflow for project setup, worldbuilding, outlining, chapter drafting, automated continuation, reader feedback, and rewrite maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[228998098](https://clawhub.ai/user/228998098)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and OpenClaw-compatible agent users use this skill to create and continue Chinese long-form novel projects with structured multi-agent support. It is intended for novel workflows that need worldbuilding, character design, outline planning, chapter writing, continuity checks, reader simulation, rolling summaries, and rewrite maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read OpenClaw configuration files that may contain API keys or provider secrets.

Mitigation: Expose only non-sensitive model metadata or manually enter model IDs, and strip fields such as apiKey, token, secret, and password before sharing configuration with child-agent prompts.

Risk: The workflow can start background child-agent sessions for style research and writing support using project details.

Mitigation: Review the spawned prompts, limit shared project context to what the task needs, and use host-level timeout and cleanup controls for background sessions.

Risk: Long-running novel generation can drift from the project outline, style anchor, or continuity state.

Mitigation: Use the included workflow state, iron rules, rolling summaries, reviewer checks, and milestone audits before accepting generated chapters or rewrites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/228998098/skills/12agent-novel)
- [Skill definition](artifact/SKILL.md)
- [Version 2.8.0 release notes](artifact/VERSION-2.8.0.md)
- [Workflow state machine](artifact/references/workflow-state-machine.md)
- [Resume protocol](artifact/references/resume-protocol.md)
- [Context feeding strategy](artifact/references/context-feeding-strategy.md)
- [Model configuration guidance](artifact/references/model-config.md)
- [Early style research parallelization](artifact/optimizations/early-style-research-parallel.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration notes, and generated project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize local project templates and coordinate background child-agent work; sensitive configuration values should be filtered before being included in prompts.]

## Skill Version(s):

2.8.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

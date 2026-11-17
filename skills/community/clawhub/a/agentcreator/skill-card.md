## Description:

Generates independent, domain-specific OpenClaw agents with dynamic core files, sandbox validation, risk review, and deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovesunshine0](https://clawhub.ai/user/lovesunshine0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace maintainers use this skill to create specialized agents from short role descriptions, including generated workspace files, review checkpoints, and deployment records. It is intended for agent-building workflows that need sandbox staging, domain-specific file generation, and explicit confirmation before persistent workspace changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-activate, persist learned state, and bypass confirmations when OPENCLAWS_AUTO_CONFIRM=true.

Mitigation: Review the skill before installing it in shared or production OpenClaw workspaces, keep OPENCLAWS_AUTO_CONFIRM unset outside isolated tests, and require explicit approval before deployment or persistent memory writes.

Risk: The workflow can write to persistent OpenClaw files such as TEAM.md, MEMORY.md, and failure_patterns.json.

Mitigation: Use review and rollback controls for persistent workspace changes, and inspect proposed file updates before allowing final deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovesunshine0/skills/agentcreator)
- [Skill Definition](artifact/SKILL.md)
- [Skill Metadata](artifact/ext/SKILL_METADATA.md)
- [Dynamic File Strategy](artifact/ext/SKILL_DYNAMIC_FILES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell commands, configuration templates, and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a staged set of agent workspace files and may propose persistent workspace updates after review and confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

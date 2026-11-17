## Description:

Adaptive Skill Stack is a meta-skill that analyzes each request, combines existing capabilities or constructs new ones, and persists learned capabilities, protocols, scripts, templates, and knowledge outside its core skill definition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to adapt across compound tasks, choose or build reusable capabilities, and maintain an evolving registry of methods and resources. It is most relevant when persistent skill growth is desired and file writes can be reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write long-lived task-derived knowledge, protocols, scripts, and templates without clear approval boundaries.

Mitigation: Run it only where persistent writes are intended, require review before each write, or disable persistence.

Risk: Sensitive or proprietary prompt content could be retained in skill files.

Mitigation: Avoid using sensitive inputs with this skill and review or redact generated knowledge before keeping or sharing it.

Risk: The artifact contains internal refusal language around editing SKILL.md that could conflict with maintainer authority.

Mitigation: Ensure authorized maintainers can edit, replace, or remove the skill definition according to platform and repository policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/adaptive-skill-stack)
- [Publisher Profile](https://clawhub.ai/user/wangjiaocheng)
- [Capability Registry](references/capability-registry.md)
- [Adaptive Protocols](references/protocols.md)
- [Knowledge Library README](references/knowledge/README.md)
- [Capability Tracker Script](scripts/capability-tracker.py)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown responses with optional code blocks, shell commands, and file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist task-derived capabilities, protocols, scripts, templates, or knowledge files when persistence is enabled.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

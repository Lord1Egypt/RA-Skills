## Description:

Compile multi-format documents into local queryable knowledge bases and manage persistent AI memory tiers using Aura Core with zero network requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auralithinc](https://clawhub.ai/user/auralithinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to compile local folders into searchable .aura knowledge bases and let agents write, query, and prune durable memory across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store user preferences, project facts, decisions, or other sensitive local data under ~/.aura/memory/.

Mitigation: Require explicit confirmation before persistent fact writes, inspect stored memory periodically, prune unwanted entries, or delete ~/.aura/memory/ to clear stored memory.

Risk: Directory compilation can index broad local folders and create searchable archives that may include secrets or sensitive documents.

Mitigation: Compile only intended directories, avoid secret-bearing paths, enable PII masking when appropriate, and review generated archives before relying on them.

Risk: The skill relies on the external auralith-aura dependency, which server security guidance says should be pinned and reviewed.

Mitigation: Install in a virtual environment, pin the dependency version, and review dependency updates before deployment.

## Reference(s):

- [Aura for OpenClaw on ClawHub](https://clawhub.ai/auralithinc/skills/aura-openclaw)
- [Aura Documentation](https://aura.rtalabs.org)
- [auralith-aura on PyPI](https://pypi.org/project/auralith-aura/)
- [Aura Core](https://github.com/Rtalabs-ai/aura-core)
- [OMNI Platform](https://omni.rtalabs.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local scripts that create .aura archives and write or manage memory under ~/.aura/memory/.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

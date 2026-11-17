## Description:

Auto-generate document index tables (ADR, RFC, Pitfall, etc.) from file frontmatter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erergb](https://clawhub.ai/user/erergb)

### License/Terms of Use:

MIT

## Use Case:

Developers and documentation maintainers use this skill to replace hand-maintained README index tables with generated tables derived from document frontmatter. It is suited for ADR, RFC, pitfall, design document, and similar file-system-based documentation directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator is commonly run through an unpinned tsx runner.

Mitigation: Pin tsx in the target project or run it through a lockfile-backed package script.

Risk: Generated README changes can publish incorrect indexes if source frontmatter or marker placement is wrong.

Mitigation: Use trusted documentation inputs, ensure each README has exactly one correctly ordered marker pair, and review generated README diffs before committing or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erergb/skills/auto-doc-index)
- [SkillKit](https://github.com/nicholasbarger/skillkit)
- [Template generator script](template/generate-doc-index.ts)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript generator code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates marker-bounded README index tables from local Markdown frontmatter; review generated diffs before committing or publishing.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

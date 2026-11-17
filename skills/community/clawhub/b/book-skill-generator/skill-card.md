## Description:

Book Skill Generator helps an agent extract core methodologies from books or user-provided book files and generate installable agent skills for those methodologies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan526](https://clawhub.ai/user/ivan526)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and external users use this skill to turn business, management, personal growth, technical, or other methodology-focused books into structured methodology lists and generated agent skills. It can work from uploaded book files or book-title research, then produce skill files, markdown guidance, packaging commands, and installation instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read book files supplied by the user and extract content from them.

Mitigation: Use it only with files you are allowed to process and avoid providing confidential or regulated content unless the agent environment is approved for that data.

Risk: The skill may search the web for methodology information when no book file is provided, which can introduce inaccurate or poorly sourced summaries.

Mitigation: Prefer uploaded source files when accuracy matters and review generated methodologies against the original book or authoritative references.

Risk: The artifact includes an unpinned npx installer command in its installation guidance.

Mitigation: Verify the installer package, version, registry, and source repository before running the command, especially in sensitive environments.

Risk: Generated skills may encode misleading or overconfident interpretations of a book's methods.

Mitigation: Review generated SKILL.md files and methodology lists before installing or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivan526/skills/book-skill-generator)
- [Artifact README](artifact/README.md)
- [Lean Startup methodology example list](artifact/examples/精益创业/方法论清单.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, generated SKILL.md content, shell command blocks, and installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create multiple methodology-specific skill folders and packageable .skill outputs from a single book.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact package.json and CHANGELOG show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

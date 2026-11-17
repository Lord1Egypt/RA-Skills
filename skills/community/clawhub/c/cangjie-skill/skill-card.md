## Description:

Cangjie Skill distills book-length source material into reusable, callable agent skill packs with structured extraction, verification, testing, learning notes, and talking points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrybenedict0515](https://clawhub.ai/user/terrybenedict0515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn a provided book or long-form source text into a structured repository of reusable AI skills, including overview notes, linked skill modules, test prompts, learning notes, and talking points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted book text can be transformed into persistent future agent instructions without explicit prompt-injection safeguards.

Mitigation: Use trusted or reviewed source texts, inspect generated SKILL.md files before loading or sharing them, and avoid adversarial documents until the workflow adds explicit untrusted-content handling.

Risk: Generated skill files may encode incorrect or misleading methodology if the source material or extracted candidates are low quality.

Mitigation: Review generated skills and test prompts before deployment, and use the workflow's candidate rejection, triple verification, and pressure-testing steps before relying on outputs.

## Reference(s):

- [Cangjie Skill ClawHub release](https://clawhub.ai/terrybenedict0515/skills/cangjie-skill)
- [Publisher profile](https://clawhub.ai/user/terrybenedict0515)
- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)
- [darwin-skill](https://github.com/alchaincyf/darwin-skill)
- [Claude Code](https://code.claude.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files organized as generated skill directories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit-oriented candidate and rejected-item folders, generated SKILL.md files, test-prompts.json files, an index, learning notes, and talking points.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

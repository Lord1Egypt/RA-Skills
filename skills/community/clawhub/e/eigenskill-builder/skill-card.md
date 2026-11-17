## Description:

Meta-skill for building and publishing agent skills on ClawHub, covering skill structure, YAML frontmatter, references directories, negative boundaries, installation instructions, ClawHub CLI workflow, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent authors use this skill to create, validate, and publish ClawHub skills with clear trigger boundaries, required frontmatter, reference-file conventions, and release quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to suggest ClawHub publish, install, or broad update commands that change published or installed skills.

Mitigation: Run publish, install, or update commands only when those changes are intended, and prefer dry-run validation before publishing.

Risk: Newly generated skills may accidentally include secrets, credentials, or other sensitive material before release.

Mitigation: Review and scan generated skill files for secrets before publishing.

Risk: Skill-design guidance can produce incorrect or misleading boundaries if applied without review.

Mitigation: Review generated descriptions, negative boundaries, and examples before deploying or publishing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/eigenskill-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with example YAML, directory layouts, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agent-authored files and commands; generated content should be reviewed before publishing.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Donad Skill helps agents generate OpenClaw skill scaffolds, validate skill structure, improve SKILL.md content, generate command frameworks and tips, and prepare publish checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onad1ocrypto](https://clawhub.ai/user/onad1ocrypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to scaffold OpenClaw skills, validate their file structure, generate bash command frameworks and tips, and manage simple local data-log workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists local plaintext data and command history, which may capture sensitive records if users log them.

Mitigation: Avoid storing secrets or private records, and set SKILL_TEMPLATE_DIR to an isolated location before use.

Risk: The advertised purpose does not match all observed behavior, including simple data-log commands alongside scaffold generation.

Mitigation: Review the skill behavior and generated files before installing, publishing, or reusing its output.

Risk: Generated downstream skill templates include a BytesAgain brand footer.

Mitigation: Remove or update the generated brand footer before publishing downstream skills.

## Reference(s):

- [Donad Skill on ClawHub](https://clawhub.ai/onad1ocrypto/skills/donad-skill)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command snippets and generated file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local plaintext data.log and history.log files when its CLI data-log commands are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

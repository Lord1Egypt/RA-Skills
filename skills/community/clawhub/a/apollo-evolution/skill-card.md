## Description:

Apollo Evolution helps agents optimize skills through an evolution-inspired cycle of copying, mutating, testing, and selecting skill variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to organize iterative skill improvement through copy, mutation, testing, and selection workflows. It is suited for experimenting with prompt, parameter, and structure changes while preserving generation state for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evolution script has unsafe input handling that can write outside intended paths or execute commands through crafted selection input.

Mitigation: Run the script only in a disposable or version-controlled workspace, pass only trusted skill names and selection values, and review filesystem changes before deploying evolved skills.

Risk: The script reports mock fitness scores until real validation and input checks are added.

Mitigation: Treat generated scores as placeholders and require independent validation before selecting or publishing an evolved skill variant.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nic-yuan/skills/apollo-evolution)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the included shell script is run, it can create copied skill variants and evolution state files under a local .memory/evolution directory.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

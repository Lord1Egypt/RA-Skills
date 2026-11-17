## Description:

Generate McKinsey-style consulting PPTs with python-pptx. Produces professional, elegant presentations with cover, content slides, and ending page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxpj](https://clawhub.ai/user/frankxpj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn structured presentation content into consulting-style PowerPoint decks with cover, summary, card, list, table, text, and closing slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime dependency is installed by the user and may vary across environments.

Mitigation: Install dependencies in a virtual environment and prefer pinned package versions before generating decks.

Risk: Generated decks may include Chinese template text and a default confidentiality footer that may not match the intended audience.

Mitigation: Review the generated deck and adjust the content or script defaults before sharing externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankxpj/skills/create-mckinsey-ppt)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [PowerPoint .pptx file generated from JSON content, with Markdown instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and python-pptx; generated decks use 16:9 slides and include default footer and closing-slide text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

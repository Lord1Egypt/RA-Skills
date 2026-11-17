## Description:

Recipe: Search your knowledge base, synthesize findings, and run a Recipe workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search a DeepVista knowledge base, summarize relevant cards, and pass the findings into a selected Recipe workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running a Recipe can expose the full knowledge base to that Recipe, even when the input focuses on selected cards.

Mitigation: Install only from a trusted DeepVista CLI package source, confirm before running a Recipe, and avoid using untrusted Recipes with sensitive workspaces.

## Reference(s):

- [DeepVista CLI](https://cli.deepvista.ai)
- [ClawHub Skill Page](https://clawhub.ai/jingconan/skills/deepvista-recipe-research-to-recipe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the DeepVista CLI and the deepvista-vistabase and deepvista-recipe skills.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

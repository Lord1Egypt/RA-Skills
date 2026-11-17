## Description:

Persona: Knowledge worker daily workflow for checking cards, processing notes, and running Recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to follow a DeepVista knowledge-work routine: review priority cards, search context, capture notes, run Recipes, and ask DeepVista chat for synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party DeepVista CLI package and uses it to handle cards, notes, recipes, chat content, and accumulated memory.

Mitigation: Install only from a trusted DeepVista CLI source and prefer a pinned, reviewed version or an installation process with lockfile or hash verification.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [ClawHub skill page](https://clawhub.ai/jingconan/skills/deepvista-persona-knowledge-worker)
- [ClawHub publisher profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the DeepVista CLI and the deepvista-vistabase, deepvista-recipe, and deepvista-notes skills.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

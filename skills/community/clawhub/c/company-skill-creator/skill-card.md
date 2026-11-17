## Description:

Creates company-internal skills interactively by guiding users through requirements gathering, scaffolding, reference creation, validation, and packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opentouchtouch](https://clawhub.ai/user/opentouchtouch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and internal enablement teams use this skill to turn company workflow, API, schema, and process knowledge into reusable agent skills. It helps collect source material, generate missing references or scripts, scaffold the skill structure, validate frontmatter, and package the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads internal documentation or other company material supplied by the user.

Mitigation: Do not provide live credentials, private keys, or unnecessary sensitive content; limit inputs to material needed for the target skill.

Risk: The skill writes generated files and may package skill directories.

Mitigation: Use a dedicated output folder and review generated scripts, references, and packaged contents before installation or sharing.

Risk: Packaging folders that contain symlinks may include unintended file content until helper scripts are hardened.

Mitigation: Avoid packaging skill folders with symlinks and inspect package contents before distribution.

## Reference(s):

- [Company Context Template](artifact/references/company-context.md)
- [Interviewer Agent](artifact/agents/interviewer.md)
- [ClawHub Skill Page](https://clawhub.ai/opentouchtouch/skills/company-skill-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SKILL.md, reference files, scripts, asset templates, validation results, and .skill packages in user-selected output folders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

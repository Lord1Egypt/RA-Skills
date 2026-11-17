## Description:

Generates branded CompleteTech Agentic Development Services Agreement packages from approved provider, client, project, commercial, and governance terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, business operators, and service teams use this skill to turn approved engagement details into draft agreement packages for agentic workflow projects, including PDF contracts, filled Markdown source, and optional envelope output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated contracts may be mistaken for legal advice or final production terms.

Mitigation: Preserve demonstration disclaimers unless counsel-reviewed replacement terms are supplied, and review generated contracts with qualified counsel before real engagements.

Risk: Generated PDF or Markdown files can replace existing files when output paths collide.

Mitigation: Use a dedicated output folder and avoid pointing outputs at important existing files or client-specific artifacts.

Risk: Contract details, contact information, and commercial terms are saved into local PDF and Markdown files.

Mitigation: Store generated outputs in appropriately access-controlled locations and share them only through approved review or signature workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/completetech/skills/agentic-contract-skill)
- [Project Homepage](https://github.com/CompleteTech-LLC/agentic-contract-skill)
- [Agentic Development Agreement Template](references/agentic_development_agreement.md)
- [References README](references/README.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are PDF, filled Markdown, and optional envelope PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file generation using user-selected config and output paths.]

## Skill Version(s):

1.0.9 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

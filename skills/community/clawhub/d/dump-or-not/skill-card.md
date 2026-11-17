## Description:

A Chinese-language relationship decision assistant that analyzes relationship descriptions or chat records across structured dimensions and gives direct breakup-or-stay guidance with a diagnostic card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sachi-pp](https://clawhub.ai/user/sachi-pp)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to describe relationship uncertainty or provide chat records, then receive structured relationship analysis, follow-up questions when key facts are missing, and direct guidance on whether to continue or end the relationship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process intimate relationship chats or screenshots.

Mitigation: Avoid sharing unnecessary personal identifiers and review any chat excerpts before submitting them to the agent.

Risk: The diagnostic card workflow can leave generated HTML or image files in temporary and media directories.

Mitigation: Delete generated files after use and avoid rendering cards from content that should not be stored or shared.

Risk: The rendering workflow starts a local HTTP server for card capture.

Mitigation: Run the workflow only in a trusted local environment and stop the server after rendering.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Assessment Dimensions](artifact/references/dimensions.md)
- [Veto Conditions](artifact/references/veto-conditions.md)
- [Profit-Taking Breakup Scenario](artifact/references/ziying-scenario.md)
- [Diagnostic Card Rendering Guide](artifact/scripts/render.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, files]

**Output Format:** [Chinese prose and Markdown tables, followed by instructions that generate a PNG diagnostic card.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to two follow-up questions at a time before producing the final analysis.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

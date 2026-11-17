## Description:

Guides an agent through an interior design proposal workflow using Jianzhuxuezhang AI tools, including requirements briefing, inspiration collection, AI render download and organization, presentation generation, budget estimation, and delivery packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior designers and studio operators use this skill to coordinate concept proposal work for residential, villa, small commercial, and early-stage design projects. It helps structure project briefs, collect references, prepare prompts, organize AI-generated images, produce presentation materials, estimate budgets, and package deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to manage project folders, downloads, generated images, budgets, presentation files, browser use, and file packaging with broad automation.

Mitigation: Before use, explicitly restrict where files may be saved, whether browser session use is allowed, and which downloads or packaging actions require confirmation.

Risk: The security summary flags a daily scheduled download task without enough user control details.

Mitigation: Disable scheduled downloads by default and require explicit user approval for any recurring task, source selection, and destination folder.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/137984917-cyber/skills/architect-ai-workflow)
- [Jianzhuxuezhang AI Drawing Tool](https://www.jianzhuxuezhang.com/ai/draw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with workflow steps, prompts, file organization instructions, and deliverable descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in project folders, downloaded images, presentation files, budget CSVs, and packaged delivery files when the user authorizes those actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

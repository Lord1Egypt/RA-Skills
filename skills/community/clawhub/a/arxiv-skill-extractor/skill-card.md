## Description:

Automates the process of extracting reusable skill code from arXiv papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to fetch arXiv paper metadata, extract research ideas, and scaffold reusable OpenClaw skills from those papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite agent-loadable skills using untrusted paper metadata.

Mitigation: Review pending_skill_task.json, paper metadata, and generated SKILL.md content before loading or installing generated skills.

Risk: Generated skill content may contain misleading instructions or prompt-injection text copied from paper metadata.

Mitigation: Scan and manually review generated skill files before deployment, especially SKILL.md and generated runner code.

Risk: Running the skill in an important workspace can overwrite generated arXiv skill directories.

Mitigation: Run it only in a workspace where replacing generated arXiv skill directories will not destroy important work.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Generated skill files plus JSON status output and command-line logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates an agent-loadable skill directory from paper metadata.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

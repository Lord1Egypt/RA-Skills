## Description:

Auto-improve any OpenClaw skill using Karpathy's autoresearch loop by auditing structure, running representative test inputs, scoring outputs against a checklist, and keeping only targeted changes that improve results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngmeyer](https://clawhub.ai/user/ngmeyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit and iteratively improve OpenClaw skills before scale use, after model upgrades, or when output quality is inconsistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request broad access to prior session history or unrelated context while selecting test inputs.

Mitigation: Provide explicit representative test inputs and restrict review to the target skill and relevant evidence.

Risk: The skill can propose or apply changes to other skill files, which may introduce incorrect guidance.

Mitigation: Require explicit approval before file writes and review proposed diffs before deployment.

Risk: The release security verdict is suspicious because authority to modify files is ambiguous.

Mitigation: Run the skill in a controlled workspace and scan or review the optimized skill before installing it in important or private workflows.

## Reference(s):

- [Checklist Examples](artifact/references/checklist-examples.md)
- [Optimization Changelog](artifact/optimization-changelog.md)
- [ClawHub Skill Page](https://clawhub.ai/ngmeyer/skills/autoresearch-skill-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with proposed edits, scoring checklists, audit findings, and changelog entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce optimized skill files and optimization changelogs when file writes are explicitly approved.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

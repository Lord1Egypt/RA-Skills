## Description:

Orchestrates the continuous learning of new skills from arXiv papers by fetching papers, extracting candidate code or skills, and solidifying validated results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and agent maintainers use this skill to run an arXiv-driven learning cycle that finds relevant papers, extracts candidate skills, tests them, and records or commits validated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extractor-provided smoke-test commands can run local shell commands in the workspace.

Mitigation: Install and run only in a sandboxed workspace, and inspect generated skills and smoke-test commands before allowing execution.

Risk: Paper-derived extraction results may persist unsafe or low-quality generated artifacts.

Mitigation: Review, scan, and test generated artifacts before committing or using them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/arxiv-skill-learning)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON status object, console log text, generated skill files, and smoke-test shell command execution when provided by the extractor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records learned papers in workspace memory and may persist generated skill artifacts.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

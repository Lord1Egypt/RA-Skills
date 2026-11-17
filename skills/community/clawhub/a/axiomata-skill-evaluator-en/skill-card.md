## Description:

Axiomata Skill Evaluator evaluates OpenClaw skill quality with bundled Axioma 5-Dimension scoring and ISO 25010 structural checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to evaluate OpenClaw skills before publishing, during quality improvement, or as part of a skill audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluator's scores may be mistaken for a publishing approval or security guarantee.

Mitigation: Treat the reports as heuristic quality feedback and keep human review and security scanning in the release process.

Risk: Running the bundled Python scripts outside a controlled environment could rely on an untrusted or unexpected PyYAML installation.

Mitigation: Run the skill in a controlled Python environment, preferably a virtualenv with a trusted PyYAML install.

Risk: The --all mode can evaluate unintended skill directories if pointed at the wrong parent path.

Mitigation: Run the scripts only against intended skill directories and review the target path before using --all.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiomata-skill-evaluator-en)
- [ClawHub publisher profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON reports from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces heuristic quality scores, structural check summaries, and recommendations; results are quality feedback rather than a security or publishing guarantee.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

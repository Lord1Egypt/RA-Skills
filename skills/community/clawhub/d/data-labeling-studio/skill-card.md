## Description:

Intelligent data labeling and annotation toolkit supporting image, text, audio, and video with active learning and quality control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to plan and run data annotation workflows, generate example annotation outputs, check labeling quality, and prepare exports for machine learning datasets. Reviewers should treat generated labels and quality scores as draft or mock outputs unless independently verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate annotation and quality-control behavior while producing mock labels and synthetic metrics.

Mitigation: Treat outputs as drafts; require human review and independent validation before using them for training data, audits, model validation, or compliance decisions.

Risk: The scripts write annotation or report files to paths supplied by the user.

Mitigation: Use explicit output paths in a disposable or version-controlled workspace and review files before merging them into production datasets.

Risk: The skill depends on image, video, audio, and ML Python packages that expand the install surface.

Mitigation: Install in an isolated environment and pin, review, and scan dependencies before use.

## Reference(s):

- [Data Labeling Studio Skill Page](https://clawhub.ai/kaiyuelv/skills/data-labeling-studio)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON annotation or quality-report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite annotation and report files at user-specified output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

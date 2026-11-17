## Description:

Guides agents through building, cleaning, annotating, splitting, formatting, and training on custom datasets, including synthetic examples and fine-tuning preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3mper0rr](https://clawhub.ai/user/3mper0rr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML practitioners use this skill to plan and execute dataset collection, cleaning, annotation, splitting, format standardization, and training or fine-tuning preparation for custom ML workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using unlicensed, unauthorized, or restricted data can make datasets unsafe to train or share.

Mitigation: Confirm source licenses, scraping permissions, and usage restrictions before collection or publication.

Risk: Internal logs or databases may contain PII, secrets, or access-controlled information.

Mitigation: Remove sensitive data, enforce access controls, and document source restrictions before training or sharing outputs.

Risk: Preprocessing before splitting data can create train, validation, or test leakage.

Mitigation: Split train, validation, and test data before preprocessing, and version preprocessing code with the dataset.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/3mper0rr/skills/dataset-creation-skill)
- [ClawHub Homepage Metadata](https://clawhub.ai/skills/dataset-creation-training)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may rely on python3, pip, pandas, or datasets.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

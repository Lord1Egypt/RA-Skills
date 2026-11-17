## Description:

BrainRepo helps an agent create and maintain a personal Markdown knowledge repository using PARA and Zettelkasten patterns for capture, organization, review, and retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codezz](https://clawhub.ai/user/codezz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent initialize and manage a plain-text second brain at ~/Documents/brainrepo/, including quick captures, project and area notes, people records, daily and weekly reviews, and knowledge retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores broad personal knowledge as plain-text Markdown files and can include sensitive personal, relationship, health, credential, or project information.

Mitigation: Use it only for information appropriate for plain-text storage, avoid secrets and high-risk personal data, and add a separate encryption and review process for sensitive content.

Risk: The skill can create, delete, commit, and push files in ~/Documents/brainrepo/, which may expose private notes if Git sync is configured incorrectly.

Mitigation: Review generated file changes before Git commits or pushes, and confirm any remote repository is private and intended.

Risk: The fixed storage path and automatic onboarding behavior provide weak user controls around where personal data is created and managed.

Mitigation: Confirm the fixed brainrepo location before first use and periodically audit the repository contents and permissions.

## Reference(s):

- [BrainRepo ClawHub skill page](https://clawhub.ai/codezz/skills/brainrepo)
- [Structure Guide](references/structure.md)
- [Workflows](references/workflows.md)
- [Templates](assets/templates/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with file paths, templates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update Markdown files in a local Git-backed knowledge repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

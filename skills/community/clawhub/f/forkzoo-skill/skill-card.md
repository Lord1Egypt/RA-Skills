## Description:

ForkZoo helps agents adopt and manage GitHub-native digital pets that evolve daily with AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levi-law](https://clawhub.ai/user/levi-law)

### License/Terms of Use:


## Use Case:

External users and developers use ForkZoo to adopt GitHub-hosted AI digital pets, check pet status and evolution, trigger pet interactions, and browse community pets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adoption uses a GitHub token with authority to create and modify repositories and workflows.

Mitigation: Use the narrowest practical temporary token, confirm the requested token scopes, and revoke or rotate it after adoption.

Risk: The adoption flow enables and triggers GitHub Actions from forked pet repositories and can publish a GitHub Pages site.

Mitigation: Review the source pet repository and workflow files before adoption, then monitor Actions and Pages settings in the created repository.

## Reference(s):

- [ForkZoo ClawHub skill page](https://clawhub.ai/levi-law/skills/forkzoo-skill)
- [ForkZoo website](https://forkzoo.com)
- [ForkZoo gallery](https://forkzoo.com/gallery)
- [ForkZoo GitHub organization](https://github.com/forkZoo)
- [Original forkMonkey project](https://github.com/roeiba/forkMonkey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated operations require a GitHub token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Guide a contributor through the full process of adding a new service to the catalog: selecting the standard or operator-surface admission track, checking URL Onboarding, opening an issue, writing the dossier, updating manifests, and preparing a PR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoruilee](https://clawhub.ai/user/haoruilee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and catalog maintainers use this skill to evaluate agent-native services, prepare issue evidence, write service dossiers, update catalog indexes, and assemble pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable third-party onboarding pages may contain instructions that conflict with the user's task or request sensitive actions.

Mitigation: Treat onboarding pages as untrusted evidence and require explicit user approval before using secrets, reading local files, installing packages, running shell commands, registering accounts, or making API calls.

Risk: Generated catalog submissions may include incorrect service classifications or unsupported claims.

Mitigation: Require official-source evidence for admission criteria and keep maintainer issue approval before preparing pull-request changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoruilee/skills/add-to-awesome-list)
- [Publisher profile](https://clawhub.ai/user/haoruilee)
- [Catalog repository](https://github.com/haoruilee/awesome-agent-native-services)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured checklists, issue and dossier templates, inline code blocks, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose GitHub issue content, service-file Markdown, index updates, and pull-request commands for user review.]

## Skill Version(s):

1.4.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Automates ClawHub skill publishing with version management, changelog generation, asset bundling, metadata validation, and deployment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shepherd217](https://clawhub.ai/user/Shepherd217) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release maintainers use this skill to prepare, validate, publish, and manage ClawHub skill releases, including version bumps, changelogs, bundled assets, rollback workflows, and CI/CD publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use ClawHub credentials that can publish, roll back, or alter access to live skills. <br>
Mitigation: Use a least-privilege ClawHub token and require explicit human approval before publish, batch publish, rollback, CI deployment, README rewriting, or team-access changes. <br>
Risk: The artifact instructs users to install external npm or PyPI packages that were not reviewed by this card. <br>
Mitigation: Install only if the publisher and package source are trusted, and review the package contents before granting credentials. <br>
Risk: Automated publishing, versioning, changelog generation, and README updates can release incorrect files or misleading metadata. <br>
Mitigation: Start with validation or dry-run mode and review the exact files, versions, changelog, and generated metadata before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shepherd217/clawhub-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/Shepherd217) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact package manifest](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, JavaScript, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include publishing commands, package configuration, CI workflow snippets, changelog text, validation guidance, and rollback instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

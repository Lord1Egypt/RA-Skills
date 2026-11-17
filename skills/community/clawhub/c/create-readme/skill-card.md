## Description:

Use when generating or updating a project README.md or CHANGELOG.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to generate or refresh evidence-based README and CHANGELOG documentation for software repositories. It supports repository discovery, README authoring, changelog authoring, bilingual documentation layout, and delivery verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation can make unsupported or misleading claims if repository evidence is incomplete or misread.

Mitigation: Review the Discovery Summary and require substantive README and CHANGELOG claims to trace to files, commits, or configuration before accepting changes.

Risk: The workflow can propose operational repository changes such as branch creation, file edits, and local git commits.

Mitigation: Tell the agent not to create branches or commits unless explicitly approved, and review diffs before accepting repository changes.

Risk: Bilingual README and auxiliary docs can diverge if one language is edited without the other.

Mitigation: Review English and Portuguese outputs together and keep linked counterpart files synchronized.

## Reference(s):

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Shields.io](https://shields.io/)
- [Make a README](https://www.makeareadme.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documents with inline shell commands and repository-specific guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write README.md, README.pt-br.md, docs files, and CHANGELOG.md after repository discovery and review checkpoints.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata; artifact frontmatter metadata reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

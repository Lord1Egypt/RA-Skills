## Description:

Generates structured Chinese changelogs and release notes from Git commits, feature lists, or code-change summaries, with categories such as additions, fixes, optimizations, and breaking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olina1ye](https://clawhub.ai/user/olina1ye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, technical leads, and operations teams use this skill to draft Chinese changelogs and release notes from commit logs, feature lists, or code-change summaries before a release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated release notes may expose sensitive internal commit details or code-change summaries.

Mitigation: Review and redact generated text before publishing.

Risk: Automated summaries can misclassify or overstate release changes.

Mitigation: Compare generated changelog entries against the source commits or change list before release.

## Reference(s):

- [Artifact skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/olina1ye/skills/changelog-generator-zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Chinese Markdown changelog or release notes; Word document export when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can organize changes by additions, fixes, optimizations, breaking changes, and other release-note categories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

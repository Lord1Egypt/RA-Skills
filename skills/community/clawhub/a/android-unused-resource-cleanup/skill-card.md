## Description:

Analyzes Android project Git changes to identify resource files that appear unused after recent edits and checks whether they are still referenced elsewhere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opoojkk](https://clawhub.ai/user/opoojkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Android engineers use this skill to review recent staged, unstaged, or historical Git changes and find Android resources that may be safe to remove after manual confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local helper reads Git diffs and Android source/resource files under the project it is run against.

Mitigation: Run it only on Android projects where local repository scanning is acceptable.

Risk: Resource cleanup suggestions may be incomplete or incorrect, especially for dynamic, reflective, or cross-module references.

Mitigation: Review the listed resources manually and build or test the project before removing anything.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/opoojkk/skills/android-unused-resource-cleanup)
- [Publisher profile](https://clawhub.ai/user/opoojkk)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown-style terminal report with suggested deletion commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions are advisory and should be manually reviewed before deleting resources.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

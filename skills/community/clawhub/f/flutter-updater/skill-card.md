## Description:

Keep Flutter/Dart projects automatically up-to-date by checking SDK releases, updating dependencies with breaking-change handling, applying fixes, and running QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaekyung-you](https://clawhub.ai/user/jaekyung-you)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers maintaining Flutter or Dart projects use this skill to update the Flutter SDK and pub dependencies, handle breaking changes with review points, run Dart/Flutter fixes, and produce a QA report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run helper programs resolved through PATH before user confirmation.

Mitigation: Use it only in a clean, backed-up Flutter/Dart workspace and verify installed helper binaries and PATH resolution before running.

Risk: The update workflow can make broad changes to project dependencies, source code, tests, build outputs, and updater state.

Mitigation: Review proposed breaking-change migrations, keep backups or version-control checkpoints outside the skill workflow, and inspect the generated QA report before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaekyung-you/skills/flutter-updater)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and conversational guidance with shell commands and file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change pubspec files, lockfiles, source and test code, SDK state, build artifacts, and .flutter_updater reports or state.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

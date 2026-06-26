## Description: <br>
Keep Flutter/Dart projects automatically up-to-date by checking SDK releases, updating dependencies, handling breaking changes, running dart fixes, and performing QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaekyung-you](https://clawhub.ai/user/jaekyung-you) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill from a Flutter or Dart project root to update the Flutter SDK, update pub.dev dependencies, migrate breaking changes when possible, run dart fix, and verify the result with analysis, tests, and builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs flutter-updater helper binaries that are not included in the reviewed package before changing project files. <br>
Mitigation: Install only from a trusted source, inspect or verify the helper binaries before use, and run the skill only in projects where these helper programs are trusted. <br>
Risk: The workflow can upgrade dependencies, edit source files, run dart fix, run tests and builds, write local state, and save a report. <br>
Mitigation: Run it from the intended Flutter or Dart project root with version control available, review user confirmation prompts, and inspect the final report and diff before accepting the changes. <br>
Risk: The workflow may rely on network lookups for SDK releases and package changelogs. <br>
Mitigation: Review fetched release and changelog information before applying breaking-change migrations, and skip or retry steps when network results are unavailable or unclear. <br>


## Reference(s): <br>
- [Flutter Updater README](artifact/README.md) <br>
- [Flutter Updater Changelog](artifact/CHANGELOG.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaekyung-you/flutter-updater) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal summaries, shell command output, and project file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update pubspec files and source files, run Flutter and Dart QA commands, write local updater state, and save a Markdown report.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

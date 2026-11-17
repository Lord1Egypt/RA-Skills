## Description:

Advanced English polish skill for non-native writing. Nativization, style consistency, diff output. CLI scripts: detector.py + polish.py

This skill is ready for commercial/non-commercial use.

## Publisher:

[muchenhengxin](https://clawhub.ai/user/muchenhengxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, writers, editors, and developers use this skill to detect Chinese-influenced English patterns and polish non-native technical or analytical English while preserving meaning, argument structure, and author voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local-file handling in report and diff helpers may be risky on shared machines or when processing sensitive documents.

Mitigation: Review before installation, avoid elevated privileges, and prefer a patched version that uses temporary or in-memory diff handling.

Risk: Generated HTML reports and broad custom regex patterns can create avoidable exposure when inputs or filenames are untrusted.

Mitigation: Avoid untrusted filenames and broad custom patterns, and prefer HTML escaping before opening generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muchenhengxin/skills/english-polish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, edited text, unified diffs, text or ANSI reports, HTML reports, and JSON batch reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detector output includes a 0-5 nativization score; report diff output is capped at 80 lines by default.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

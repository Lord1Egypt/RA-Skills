## Description:

Validates CHANGELOG.md files against Keep a Changelog conventions, including version ordering, date formats, section types, link references, and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to lint CHANGELOG.md files before release, review changelog structure, and generate text, JSON, or Markdown issue reports for local or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python linter against a changelog path supplied by the user.

Mitigation: Review the installed script before use and run it only against intended changelog files in the target workspace.

Risk: CI use can block a release when changelog errors are found or when strict mode treats warnings as failures.

Mitigation: Adopt strict mode deliberately and review reported issues before treating them as release blockers.

## Reference(s):

- [Keep a Changelog](https://keepachangelog.com)
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/changelog-linter)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown lint reports with issue summaries, version listings, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The linter returns exit code 1 when errors are found, and strict mode also fails on warnings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

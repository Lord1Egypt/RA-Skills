## Description: <br>
Validate CHANGELOG.md files against the Keep a Changelog format, including version ordering, date formats, section types, link references, and formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to lint CHANGELOG.md files, inspect release versions, validate ordering, and check version link references before publishing or running CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strict CI usage can block builds on warnings. <br>
Mitigation: Enable --strict only when the project is ready to treat changelog warnings as build-blocking issues. <br>
Risk: Lint findings may be inaccurate if the input is not a changelog or intentionally diverges from Keep a Changelog conventions. <br>
Mitigation: Run the skill only on changelog files intended for this format and review reported issues before changing release notes. <br>


## Reference(s): <br>
- [Keep a Changelog](https://keepachangelog.com) <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/changelog-linter) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown lint results with issue summaries and version lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected changelog file locally and returns lint findings; no network, credential, hidden, or persistence behavior is reported by evidence.security.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

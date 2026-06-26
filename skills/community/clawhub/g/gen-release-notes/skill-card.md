## Description: <br>
Generates release notes for changes since a given tag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to analyze git history since a previous tag, draft Keep a Changelog release notes, update CHANGELOG.md, and verify compare links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changelog edits can be incorrect or misleading if the selected previous tag or git history analysis is wrong. <br>
Mitigation: Provide the intended previous tag, stop if the tag gate fails, and review the generated CHANGELOG.md diff before committing. <br>
Risk: Merged pull request metadata may be unavailable when the GitHub CLI query fails. <br>
Mitigation: Use commit subjects and merge-commit URLs as fallback evidence, and do not fabricate PR numbers or links. <br>
Risk: Footer compare links can be missing or point at the wrong version range. <br>
Mitigation: Run the staged CHANGELOG.md footer gate and correct the footer until both compare-link checks pass. <br>


## Reference(s): <br>
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) <br>
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/gen-release-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown release notes with inline shell commands and changelog footer guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update CHANGELOG.md; generated diffs and footer compare links should be reviewed before committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

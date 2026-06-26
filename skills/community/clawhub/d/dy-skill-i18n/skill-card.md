## Description: <br>
Helps developers internationalize frontend applications by identifying hardcoded UI text, reusing or adding locale entries, replacing strings with project-specific i18n calls, and checking translation completeness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyaoqi](https://clawhub.ai/user/anyaoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when adapting frontend codebases for multilingual support. It guides locale-file placement, translation-key reuse or creation, hardcoded-string replacement, and post-change validation while preserving existing project conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify frontend source and localization files. <br>
Mitigation: Review the diff before applying changes, and clarify when only translation advice is desired. <br>
Risk: Incorrect translations or misplaced keys can cause confusing UI text or missing translation warnings. <br>
Mitigation: Validate translated pages by switching languages, checking supported locale files for matching keys, and running the project's lint or test tools when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anyaoqi/dy-skill-i18n) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and proposed source or locale file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update frontend source files and localization files; users should review diffs before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

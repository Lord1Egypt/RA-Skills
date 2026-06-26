## Description: <br>
Keeps project documentation in sync with code changes by identifying stale docs, drafting updates, and maintaining doc site navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chriscox](https://clawhub.ai/user/chriscox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to audit stale project documentation, update affected docs after code or PR changes, and keep mkdocs, Docusaurus, or VitePress navigation aligned with documentation files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read repository diffs and documentation and may make doc-related changes when the user selects that workflow. <br>
Mitigation: Use review-first mode for unfamiliar or important repositories, inspect proposed diffs before applying them, and review any commits or issues before publishing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with proposed or applied file edits and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect repository diffs, documentation files, doc-site configuration, and GitHub pull request metadata through the user's authenticated GitHub CLI session.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

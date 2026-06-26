## Description: <br>
Execute coding tasks like feature implementation, bug fixes, refactoring, and code reviews using Cursor AI within specified project directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igrwijaya](https://clawhub.ai/user/igrwijaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate feature implementation, bug fixes, refactoring, tests, and code review tasks to Cursor AI within a selected project repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor AI receives full access to the selected repository and may inspect or modify project files while completing the requested coding task. <br>
Mitigation: Run it on a feature branch or other reviewed branch, review all diffs before commits or pushes, and avoid production branches. <br>
Risk: Task text, repository contents, and optional credentials may be exposed to the Cursor agent workflow. <br>
Mitigation: Do not include secrets in task text, keep sensitive credentials out of the repository, verify the cursor-agent package source and version, and scope CURSOR_API_KEY appropriately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igrwijaya/coding-with-cursor-ai) <br>
- [Publisher profile](https://clawhub.ai/user/igrwijaya) <br>
- [Cursor CLI](https://cursor.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task summaries, shell output, code edits, commits, and pull request summaries produced through Cursor AI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local project path, natural-language task, optional focused file list, cursor-agent on PATH, and optional CURSOR_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

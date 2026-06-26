## Description: <br>
Use when adding new AI/startup directories to directories.json from a URL, pasted text, or GitHub awesome-list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[man0l](https://clawhub.ai/user/man0l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and growth teams use this skill to add AI or startup directory entries from URLs, pasted text, or GitHub lists, then deduplicate and classify them in a local directory dataset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from directory parsing into external submissions, credentialed browser sessions, file uploads, GitHub forks, pushes, or PR creation. <br>
Mitigation: Require explicit user approval before any external submission, credential use, upload, fork, push, or PR, and review the local scripts before running them. <br>
Risk: Automated browser verification and form discovery may interact with third-party sites and submission forms. <br>
Mitigation: Use the workflow for parsing and classification first, then separately approve and supervise any browser automation that contacts external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/man0l/add-directories) <br>
- [Publisher profile](https://clawhub.ai/user/man0l) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to directories.json and commands for local analysis, cleanup, browser verification, form discovery, and submission workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Crayfish Diary helps an agent record diary entries, memos, todos, and meeting notes into local Markdown files organized by year, month, and day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[italks](https://clawhub.ai/user/italks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and other users can use this skill to capture personal diary notes, quick memos, todos, and meeting notes. The skill formats entries as Markdown, stores them in dated local folders, and maintains a daily README summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary entries may persist personal, confidential, or regulated information in local Markdown files. <br>
Mitigation: Choose the storage location deliberately, avoid secrets or regulated data unless retention is intended, and review or delete generated files when needed. <br>
Risk: Broad recording triggers can capture more conversation content than the user intended. <br>
Mitigation: Start recording deliberately, stop recording promptly, and confirm the captured content before relying on it as a record. <br>
Risk: The bundled publishing script can commit and push files to a configured GitHub repository. <br>
Mitigation: Do not run the publishing script unless the repository, remote, and staged changes have been reviewed. <br>


## Reference(s): <br>
- [Crayfish Diary on ClawHub](https://clawhub.ai/italks/crayfish-diary) <br>
- [italks publisher profile](https://clawhub.ai/user/italks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diary files, daily Markdown summaries, and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local year/month/day folders and Markdown files when used with file-writing tools; optional publishing guidance may involve git commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Preview git diffs and files using the diff4 CLI for secure code change and file review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djyde](https://clawhub.ai/user/djyde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to share git diffs, staged changes, or selected UTF-8 text files through the diff4 CLI so reviewers can inspect encrypted content by URL with an out-of-band passphrase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected diffs or files can leave the user's machine as encrypted uploads. <br>
Mitigation: Confirm the exact files, diff scope, and server before each share. <br>
Risk: Passphrase setup or retrieval can expose the encryption passphrase during normal use. <br>
Mitigation: Run key generation or retrieval only after explicit approval, and avoid sharing the passphrase in chat or logs. <br>


## Reference(s): <br>
- [diff4 service](https://diff4.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and returned URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce share URLs for encrypted uploads; recipients need the passphrase out of band.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

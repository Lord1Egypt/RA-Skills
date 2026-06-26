## Description: <br>
Send local files to nearby Apple devices through AirDrop with macOS guardrails, staging checks, and automation-friendly workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill on macOS to stage exact local files and open the native AirDrop chooser or a user-owned Shortcut for nearby Apple-device handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved files may be sent to the wrong nearby recipient if the user selects the wrong device in the macOS AirDrop chooser. <br>
Mitigation: Keep recipient selection interactive and ask the user to confirm the exact payload before launch, especially for private files. <br>
Risk: Staged files in ~/airdrop/staging may retain sensitive content after sharing. <br>
Mitigation: Use staging only for approved payloads and delete staging files after use when they contain sensitive material. <br>
Risk: Folders, logs, or bundles can include hidden files, credentials, or unrelated workspace content. <br>
Mitigation: Resolve exact file paths, prefer curated archives, and exclude credentials, hidden files, and unrelated state unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/airdrop) <br>
- [Skill homepage](https://clawic.com/skills/airdrop) <br>
- [Workflow Recipes - AirDrop](workflow-recipes.md) <br>
- [Troubleshooting - AirDrop](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with AirDrop enabled; recipient selection remains interactive in the native macOS UI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Helps an agent guide Kuaishou login, validate account cookies, and prepare commands for uploading videos or image-note posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to prepare Kuaishou publishing workflows, check login state, and upload video or image-note content from local media files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use can download and run unpinned third-party automation code, including from proxy or mirror domains. <br>
Mitigation: Review and pin a verified source before installation, and run the automation in a controlled local environment. <br>
Risk: Stored login state can publish content to a Kuaishou account. <br>
Mitigation: Confirm the target account, media files, title, text, tags, and schedule before running upload commands. <br>
Risk: Interactive login requires a real user session and can expose account state if run in the wrong environment. <br>
Mitigation: Have the user run login locally, use separate account names for isolation, and refresh login only when cookie checks fail. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/kukuoai/deepsop-kuaishou-ai) <br>
- [Publisher profile](https://clawhub.ai/user/kukuoai) <br>
- [social-auto-upload project](https://github.com/dreammis/social-auto-upload) <br>
- [CLI contract](references/cli-contract.md) <br>
- [Runtime requirements](references/runtime-requirements.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and code templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include login commands that the user must run interactively in a local terminal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Uses the Python biliup CLI to help an agent log in to Bilibili, collect video submission details, upload local or downloaded video files, and return the upload result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PokersKun](https://clawhub.ai/user/PokersKun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to publish videos to their own Bilibili accounts from an agent workflow, including first-time QR login, upload metadata collection, and submission result reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and reuses a Bilibili login token in cookies.json. <br>
Mitigation: Run it only in a trusted workspace, keep cookies.json out of version control, and remove or rotate the token when it is no longer needed. <br>
Risk: The skill can install Python packages and helper dependencies. <br>
Mitigation: Review the setup commands before execution and prefer an isolated Python environment or pipx installation. <br>
Risk: The skill may download media from provided URLs before upload. <br>
Mitigation: Accept downloads only from trusted sources and verify the downloaded file before submitting it. <br>
Risk: The skill can post videos publicly to the user's Bilibili account. <br>
Mitigation: Require a final human review of title, tags, category, copyright settings, and target files before running the upload command. <br>


## Reference(s): <br>
- [biliup project](https://github.com/biliup/biliup) <br>
- [Bilibili upload category page](https://member.bilibili.com/platform/upload/video/frame) <br>
- [Bilibili category tid list](artifact/references/tid_list.md) <br>
- [ClawHub skill page](https://clawhub.ai/PokersKun/biliup-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, file paths, and upload status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a QR-code image path for login and a Bilibili BV identifier after a successful upload.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

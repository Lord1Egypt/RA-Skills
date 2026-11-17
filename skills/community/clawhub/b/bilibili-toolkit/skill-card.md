## Description: <br>
bilibili-toolkit helps agents assist with Bilibili creator operations such as video uploads, scheduled publishing, batch downloads, credential handling, and performance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to guide Bilibili video publishing, scheduled releases, batch downloads, data tracking, and related account workflows. The skill is intended for agent-assisted operation where users review account-changing actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive Bilibili session credentials and account-changing operations. <br>
Mitigation: Treat SESSDATA and bili_jct as passwords, keep them out of LLM prompts and unrelated tools, avoid credential persistence unless necessary, and require manual confirmation before upload, edit, draft, or scheduled publish actions. <br>
Risk: The skill requests command execution and file access for workflows that can affect local files and a Bilibili account. <br>
Mitigation: Install only in trusted agent environments, review requested commands and file paths before execution, and run with the least access needed for the specific task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bilibili-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration notes, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Bilibili session credentials and manual confirmation for upload, edit, draft, or scheduled publish actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

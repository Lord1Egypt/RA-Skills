## Description: <br>
Automates the BOSS Zhipin new-greeting recruiting inbox by reading candidate resumes, syncing records and attachments to Feishu, and optionally requesting missing resume attachments. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters and authorized recruiting operators use this skill to process BOSS Zhipin new-greeting inbox items, synchronize candidate profiles and resume attachments to Feishu, and keep task state across runs. Live outbound messaging is opt-in and should be used only after confirming account authority and candidate-data handling obligations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a live recruiting account and may send candidate-facing messages when run with --live. <br>
Mitigation: Use the default dry-run behavior unless the user explicitly authorizes live messaging, and start live runs with a small limit while reviewing the message text. <br>
Risk: The skill handles candidate resumes and transfers candidate data to Feishu. <br>
Mitigation: Run only for accounts and candidate data the operator is authorized to process, and confirm privacy and data-transfer obligations before syncing. <br>
Risk: The skill depends on browser session cookies and local Feishu authorization material. <br>
Mitigation: Protect local files under ~/.opencli/boss-recruit, avoid logging or committing credentials, and rotate any Feishu token used with --token. <br>
Risk: The security scan flags anti-detection behavior and platform-automation risk. <br>
Mitigation: Review platform terms before use and prefer a version that removes anti-detection guidance, plaintext token persistence, and cookie-backed download behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperkwok/skills/boss-recruit) <br>
- [OpenCLI](https://github.com/jackwener/opencli) <br>
- [Anti-detection operating notes](references/anti-detection.md) <br>
- [Agent usage notes](AGENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with shell commands and structured command output from Node scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and OpenCLI; uses local BOSS browser session state and local Feishu target configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

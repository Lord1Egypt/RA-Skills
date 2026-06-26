## Description: <br>
Provides command-line guidance for using BaiduPCS-Go to manage Baidu Netdisk files, shares, transfers, offline downloads, accounts, and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linauror](https://clawhub.ai/user/linauror) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and command-line users use this skill to operate Baidu Netdisk through BaiduPCS-Go, including uploads, downloads, transfers, sharing, quota checks, account management, and configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on raw Baidu account tokens or cookies for some login flows. <br>
Mitigation: Avoid pasting full browser cookies, BDUSS, or STOKEN values into shared shell history; use a trusted terminal and consider a dedicated low-risk account. <br>
Risk: BaiduPCS-Go performs high-impact cloud file operations such as delete, overwrite, share, recycle-bin purge, and configuration changes. <br>
Mitigation: Manually confirm the active account, target paths, and command flags before running destructive or sharing commands. <br>
Risk: The external BaiduPCS-Go executable is not verified by the release evidence. <br>
Mitigation: Install BaiduPCS-Go only from a source you trust and verify the executable when possible before using it with account credentials. <br>


## Reference(s): <br>
- [BaiduPCS-Go command reference](artifact/BaiduPCS-Go.md) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/linauror/baidupcs-go) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command options, file paths, account-token handling guidance, and safety checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

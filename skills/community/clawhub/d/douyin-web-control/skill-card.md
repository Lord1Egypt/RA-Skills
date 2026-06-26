## Description: <br>
Guides an agent to operate Douyin web through the douyin-web CLI for session launch, login checks, navigation, search, playback control, interactions, screenshots, and recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwang233](https://clawhub.ai/user/billwang233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to operate an authenticated Douyin web session through a dedicated CLI while preserving boundaries for login challenges, account-affecting actions, screenshots, and recording. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an authenticated Douyin web session and perform public account actions. <br>
Mitigation: Require explicit user confirmation before likes, follows, favorites, shares, submitted comments, or submitted danmaku. <br>
Risk: Screenshots and recordings can capture private page content or system audio. <br>
Mitigation: Treat generated screenshots and recordings as sensitive and review the target session before capture. <br>
Risk: The skill depends on an external douyin-web-cli project for browser control. <br>
Mitigation: Install and run it only when the external CLI project is trusted for the intended environment. <br>
Risk: Login, captcha, verification, or account-risk challenges may appear during automation. <br>
Mitigation: Pause automation and ask the user to complete verification manually before continuing. <br>


## Reference(s): <br>
- [Douyin Web Control release page](https://clawhub.ai/billwang233/douyin-web-control) <br>
- [Douyin Web CLI project](https://github.com/billwang233/douyin-web-cli) <br>
- [Feature Matrix](references/feature-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands may create screenshot or recording files and JSON status output.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
B站全自动签到工具 — 每日经验任务（登录+观看+分享+投币=65EXP/天）+ 直播间弹幕签到刷亲密度。支持UP主名字/UID查找直播间。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XiaoYiWeio](https://clawhub.ai/user/XiaoYiWeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Bilibili daily experience tasks, send live-room danmaku check-ins, and resolve creator names or UIDs to live room IDs through Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Bilibili session cookies that can authorize account access. <br>
Mitigation: Treat SESSDATA and bili_jct as passwords, avoid sharing them in chats or logs, delete .cookies.json when finished, and revoke or refresh the session if exposed. <br>
Risk: Daily tasks and danmaku check-ins can mutate the user's Bilibili account, including posting danmaku or spending coins when coin mode is enabled. <br>
Mitigation: Confirm the intended account actions before running scripts, keep coin spending disabled unless explicitly requested, and review target room IDs and messages before check-in. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/XiaoYiWeio/bili-checkin) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Bilibili](https://www.bilibili.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scripts can save local cookie credentials, query account and task status, send Bilibili API requests, and print task results for the agent to relay.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

把本机 LobsterAI 接入「无限画布」平台。首次下载连接器、启动本地服务，并生成"打开即自动连接"的画布链接；本地模式不限次数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainbow-boy-max](https://clawhub.ai/user/rainbow-boy-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to connect a local LobsterAI desktop agent to the Infinite Canvas platform, start or reuse a local connector service, and open a canvas URL that carries the connection details when safe to do so.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use downloads and runs local Node.js connector code in the background.

Mitigation: Use the skill only when the publisher and official connector distribution are trusted; review the generated start command before running it and stop the canvas-agent.mjs process when finished.

Risk: A connector token can be exposed in a generated browser URL for automatic canvas connection.

Mitigation: Avoid sharing generated pageUrl values and prefer the official canvas domain behavior that limits token-bearing URLs to the official host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rainbow-boy-max/skills/canvas-connector)
- [Publisher profile](https://clawhub.ai/user/rainbow-boy-max)
- [Infinite Canvas platform](https://aicanvas.miaotuntu.com)
- [LobsterAI desktop](https://lobsterai.youdao.com/)
- [Official connector distribution](https://aicanvas.miaotuntu.com/downloads/lobster-canvas-agent.mjs)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local connector start command and a browser page URL containing connector details for the official canvas domain.]

## Skill Version(s):

1.1.0 (source: server release metadata, VERSION, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

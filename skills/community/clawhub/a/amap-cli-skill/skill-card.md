## Description:

通过 CLI 命令行参数实时操控运行在容器中的高德地图 JSAPI 2.0 实例，支持地图状态控制、路径规划、POI 搜索等，所有操作均以结构化 JSON 输出，适合 AI Agent 驱动的地图可视化交互场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to control an AMap JSAPI map container from the command line for map viewing, route planning, POI search, and follow-up actions from user map selections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AMap API credentials may be exposed through setup or command logs.

Mitigation: Use platform-managed secret injection, avoid commands that print key values, and rotate any key that may have been printed.

Risk: The setup installs an unpinned global npm package.

Mitigation: Pin and review the @amap-lbs/amap-gui package version before installation.

Risk: The skill reads AMap credentials from ~/.openclaw/openclaw.json when environment injection is unavailable.

Mitigation: Prefer runtime environment variables or managed secrets over reading local configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbs-amap/skills/amap-cli-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/lbs-amap)
- [AMap developer portal](https://lbs.amap.com)
- [@amap-lbs/amap-gui npm package](https://www.npmjs.com/package/@amap-lbs/amap-gui)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command-result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for commands that return JSON map state, route, POI, and interaction-event data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

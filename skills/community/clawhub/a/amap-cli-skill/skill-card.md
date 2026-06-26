## Description: <br>
通过 CLI 命令行参数实时操控运行在容器中的高德地图 JSAPI 2.0 实例，支持地图状态控制、路径规划、POI 搜索等，所有操作均以结构化 JSON 输出，适合 AI Agent 驱动的地图可视化交互场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the Gaode/AMap GUI CLI, control map state, search POIs, read map interactions, and plan routes with structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access AMap API keys and exports them broadly into the shell environment. <br>
Mitigation: Review the skill before installation, prefer platform-scoped environment injection, and avoid manual credential reads from ~/.openclaw/openclaw.json where possible. <br>
Risk: Map searches, clicked POIs, and route planning can involve precise or sensitive locations. <br>
Mitigation: Avoid using sensitive home, workplace, client, or travel locations unless the user understands that location data may be sent to AMap services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbs-amap/amap-cli-skill) <br>
- [@amap-lbs/amap-gui npm package](https://www.npmjs.com/package/@amap-lbs/amap-gui) <br>
- [AMap Open Platform](https://lbs.amap.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to use amap-gui commands and summarize structured JSON outputs for map state, routes, POIs, and user map events.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

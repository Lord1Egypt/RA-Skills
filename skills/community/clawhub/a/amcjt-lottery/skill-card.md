## Description: <br>
专业彩票助手 - 支持双色球开奖查询、彩票OCR识别、中奖核对、开奖提醒。触发词：彩票、双色球、开奖、中奖、lottery。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbhim](https://clawhub.ai/user/jbhim) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to query Double Color Ball lottery results, recognize lottery ticket images, check whether selected numbers won, and view draw countdown or calendar information through a configured mcporter MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls an external MCP service through mcporter and requests broad shell command access for node, npx, and mcporter. <br>
Mitigation: Install only when the mcporter setup and amcjt-mcp-server endpoint are trusted, and review mcporter commands before execution. <br>
Risk: Uploaded lottery ticket images and lottery data may be sent to the external MCP service for OCR and prize checking. <br>
Mitigation: Do not upload ticket images or lottery data that should not be shared with that service. <br>
Risk: Troubleshooting examples include commands that can modify MCP configuration or expose API-key values. <br>
Mitigation: Avoid running configuration changes or printing and inlining real API keys unless the impact is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jbhim/amcjt-lottery) <br>
- [mcporter npm package](https://www.npmjs.com/package/mcporter) <br>
- [Model Context Protocol specification](https://github.com/modelcontextprotocol/specification) <br>
- [mcporter CLI reference](https://github.com/steipete/mcporter/blob/main/docs/cli-reference.md) <br>
- [mcporter tool calling guide](https://github.com/steipete/mcporter/blob/main/docs/tool-calling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured lottery result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include lottery numbers, draw dates, prize information, OCR results, MCP troubleshooting guidance, and mcporter command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

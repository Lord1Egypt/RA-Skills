## Description:

专业彩票助手 - 支持双色球开奖查询、彩票OCR识别、中奖核对、开奖提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbhim](https://clawhub.ai/user/jbhim)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to query Double Color Ball lottery results, recognize ticket numbers from photos, check whether entered bets won, and get draw countdown or calendar information through a configured MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is suspicious because the skill requests broader node, npx, and mcporter command authority than its lottery workflows require.

Mitigation: Review the skill before installation, run it in a tightly sandboxed OpenClaw environment, and prefer a release that removes node and npx Bash access.

Risk: The skill depends on a configured amcjt-mcp-server for lottery data, OCR, and win checking.

Mitigation: Use only a trusted amcjt-mcp-server configuration and narrow mcporter access to the listed lottery tools where possible.

Risk: Ticket photos may contain sensitive or personal information.

Mitigation: Avoid processing unrelated images or sensitive ticket photos, and do not run the skill in environments containing credentials unless needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jbhim/skills/amcjt-lottery)
- [mcporter npm package](https://www.npmjs.com/package/mcporter)
- [Model Context Protocol specification](https://github.com/modelcontextprotocol/specification)
- [mcporter CLI reference](https://github.com/steipete/mcporter/blob/main/docs/cli-reference.md)
- [mcporter tool calling guide](https://github.com/steipete/mcporter/blob/main/docs/tool-calling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include lottery result summaries, OCR number extraction, win-check results, countdown or calendar information, and mcporter configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

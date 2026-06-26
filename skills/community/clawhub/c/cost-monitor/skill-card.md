## Description: <br>
Real-time token usage and cost tracking for OpenClaw agents, with MiMo credit-plan and DeepSeek RMB balance summaries after replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengkezhou](https://clawhub.ai/user/chengkezhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor per-turn token usage, estimated costs, and remaining provider balance during normal agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps a local running balance file derived from usage metadata. <br>
Mitigation: Keep the skill directory private and delete or reset balance.json when you do not want usage-derived state retained. <br>
Risk: DeepSeek calibration can read a local OpenClaw DeepSeek API key and contact DeepSeek's balance endpoint. <br>
Mitigation: Review the calibration script and only run DeepSeek calibration when you intend to query the provider balance endpoint with that credential. <br>
Risk: The cost monitor is designed to run after every assistant reply. <br>
Mitigation: Install it only when continuous cost and balance tracking is desired, and remove the cost monitoring rule if that behavior is no longer wanted. <br>


## Reference(s): <br>
- [Cost Monitor detailed guide](references/detailed-guide.md) <br>
- [ClawHub Cost Monitor page](https://clawhub.ai/chengkezhou/cost-monitor) <br>
- [MiMo pricing reference](https://platform.xiaomimimo.com/docs/zh-CN/price/) <br>
- [DeepSeek balance endpoint](https://api.deepseek.com/user/balance) <br>
- [Publisher profile](https://clawhub.ai/user/chengkezhou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [One-line text or Markdown status summaries with optional shell commands for balance calibration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads transcript usage metadata, pricing configuration, and local balance state; optional DeepSeek calibration queries the provider balance endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

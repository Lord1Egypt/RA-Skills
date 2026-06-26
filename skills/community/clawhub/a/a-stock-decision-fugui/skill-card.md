## Description: <br>
从共享记忆读取持仓，生成 A 股投资决策报告（止损/止盈/仓位管理） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzx0385-cpu](https://clawhub.ai/user/hzx0385-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users with A-share holdings can generate a Markdown decision report that reads local portfolio data, checks current prices, and summarizes stop-loss, take-profit, and position-management signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill imports and executes an unbundled local helper from ~/.openclaw/workspace/shared_memory_loader.py at startup. <br>
Mitigation: Inspect and trust that helper before running the skill, and keep the workspace path limited to code you control. <br>
Risk: Portfolio symbols are queried through qt.gtimg.cn and reports are saved locally under ~/.openclaw/decisions. <br>
Mitigation: Run only if that data flow is acceptable, and review local file permissions for generated reports. <br>
Risk: The generated stock signals may be incomplete, stale, or unsuitable for real trading decisions. <br>
Mitigation: Treat the report as informational guidance and verify prices, holdings, and thresholds before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzx0385-cpu/a-stock-decision-fugui) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Tencent stock quote endpoint](https://qt.gtimg.cn/q={symbol}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown investment decision report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the skill also saves a timestamped Markdown report under ~/.openclaw/decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Track API spend with intent-level attribution. Shows where your tokens go by project and purpose. Invoke with /meter for spend summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oztenbot](https://clawhub.ai/user/oztenbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use AgentMeter to summarize Claude Code token usage and estimated API spend by project, model, and session. It can also install a local Stop hook for future session tracking and optionally sync usage summaries to the AgentMeter dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make local project changes by copying a Stop hook into .claude/hooks and updating .claude/settings.json. <br>
Mitigation: Review the hook and settings changes before relying on automatic tracking, and remove the Stop hook if persistent session tracking is not desired. <br>
Risk: Backfill scans historical Claude Code transcript metadata under ~/.claude/projects and stores usage summaries locally. <br>
Mitigation: Run the skill only in environments where local transcript metadata can be analyzed for spend tracking, and review ~/.agent-meter/spend.jsonl for stored fields. <br>
Risk: Optional dashboard sync uploads usage summaries and stores an API key locally. <br>
Mitigation: Use sync only with a trusted AgentMeter endpoint, protect ~/.agent-meter/sync.json, and use --dry-run or --status before sending records when needed. <br>


## Reference(s): <br>
- [ClawHub AgentMeter release page](https://clawhub.ai/oztenbot/agent-meter) <br>
- [AgentMeter dashboard](https://dashboard.agentmeter.io) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown spend summaries with shell commands and local JSONL session summary records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local spend records to ~/.agent-meter/spend.jsonl and may update .claude/settings.json when installing the Stop hook.] <br>

## Skill Version(s): <br>
0.6.4 (source: ClawHub release metadata; artifact frontmatter lists 0.6.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

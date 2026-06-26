## Description: <br>
Token Saver reduces Claude API token consumption by diagnosing waste patterns, recommending model-routing and prompt optimizations, and generating cost reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Token Saver to inspect Claude/OpenClaw usage, identify high-cost configuration patterns, and produce ranked recommendations or cost reports before approving any configuration edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ANTHROPIC_API_KEY to query Anthropic usage data and may expose sensitive usage or spend information if mishandled. <br>
Mitigation: Keep the key in the environment, consider using a least-privileged or rotated key where available, and share generated usage reports only with intended operators. <br>
Risk: The skill reads local OpenClaw prompt and configuration files to estimate token usage and identify cost drivers. <br>
Mitigation: Run it only in workspaces where the agent is allowed to inspect those local files. <br>
Risk: Approved recommendations can change openclaw.json or MEMORY.md, which may alter agent behavior or remove local memory entries. <br>
Mitigation: Review proposed diffs before approval and keep configuration or memory files under backup or version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicope/clawtrix-token-saver) <br>
- [Anthropic usage API endpoint](https://api.anthropic.com/v1/usage?days=7) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reports with inline shell commands, JSON cost-report option, and proposed configuration diffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ANTHROPIC_API_KEY for Anthropic usage data; proposed file edits require explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md Version section, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

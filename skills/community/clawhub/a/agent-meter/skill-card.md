## Description:

Track API spend with intent-level attribution. Shows where your tokens go by project and purpose. Invoke with /meter for spend summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oztenbot](https://clawhub.ai/user/oztenbot)

### License/Terms of Use:


## Use Case:

Developers and engineers use AgentMeter to install a Claude Code Stop hook, backfill local Claude Code session transcripts, estimate token spend, and view spend by day, project, and model. Users can optionally sync local spend summaries to the AgentMeter dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes lasting project configuration changes by installing a Stop hook and updating Claude settings.

Mitigation: Review the generated .claude/settings.json and .claude/hooks/meter-session-end.sh changes before continuing to use the hook.

Risk: The skill reads Claude Code transcript metadata and stores spend history locally.

Mitigation: Install only in projects where local transcript-derived spend records in ~/.agent-meter/spend.jsonl are acceptable.

Risk: Dashboard sync sends local spend summaries to an external service and uses an API key.

Mitigation: Use sync only with the default HTTPS endpoint, store a revocable API key, and run dry-run or status checks before syncing when reviewing behavior.

Risk: Unsafe argument handling may affect commands when untrusted text is passed to /meter.

Mitigation: Avoid passing untrusted /meter arguments until argument validation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oztenbot/skills/agent-meter)
- [AgentMeter dashboard](https://dashboard.agentmeter.io)
- [AgentMeter API endpoint](https://api.agentmeter.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with shell command execution and local JSONL spend records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session_summary records to ~/.agent-meter/spend.jsonl and may update .claude/settings.json and .claude/hooks/ during setup.]

## Skill Version(s):

0.6.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Audits OpenClaw Gateway cron jobs from jobs.json or the CLI, classifies scheduled workloads by token cost, and suggests when OS timers plus scripts and openclaw message send could replace recurring LLM runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x3r081](https://clawhub.ai/user/x3r081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review OpenClaw Gateway cron schedules, identify LLM-invoking recurring jobs, and decide whether deterministic OS timer plus script workflows are safer or cheaper for specific jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron job definitions may include embedded tokens, private chat IDs, or sensitive prompt text. <br>
Mitigation: Redact secrets, private identifiers, and sensitive prompt content before sharing jobs.json or CLI output with an agent. <br>
Risk: Migration guidance could lead to duplicate sends or missed schedules if a replacement timer is applied without verification. <br>
Mitigation: Keep the skill read-only, test replacement scripts manually, and disable the old Gateway cron only after confirming the new timer fires once as intended. <br>
Risk: Heuristic token-savings classifications can be wrong when a job still needs search, summarization, judgment, or variable tool use. <br>
Mitigation: Treat savings as confidence-based guidance, not a guarantee, and keep low-confidence or judgment-heavy jobs on agent cron unless a human confirms a deterministic replacement. <br>


## Reference(s): <br>
- [Reference - Cron Job Auditor](REFERENCE.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown report with per-job tables, numbered manual steps, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only advisory output; does not edit cron jobs, jobs.json, system timers, or scripts unless the user explicitly asks for a draft.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

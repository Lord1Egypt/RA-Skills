## Description: <br>
Track and analyze OpenClaw session costs by parsing transcripts, calculating per-model spend, setting budgets, and alerting on overruns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect local OpenClaw session transcripts, estimate recent token spend, summarize spend by day or model, and add budget alerts to their agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports hidden, unrelated external registration and ping metadata in an HTML comment. <br>
Mitigation: Remove or clearly explain the hidden OADP metadata before use, and do not use the listed external endpoints unless they are intentionally trusted. <br>
Risk: The example commands can scan broad local OpenClaw session paths, which may include sensitive transcripts in shared or multi-agent environments. <br>
Mitigation: Limit the session path to files you are comfortable reading and review commands before running them in sensitive environments. <br>
Risk: Cost totals depend on usage and cost fields present in local transcript records and may be incomplete. <br>
Mitigation: Treat generated totals as estimates and compare them with provider billing data before making budget or accounting decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with bash and markdown snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local cost summaries and budget-check guidance based on available OpenClaw session transcript fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Track AI agent token usage, model costs, and budget thresholds with a TypeScript and SQLite workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent engineers use this skill to add local token, cost, and budget tracking to agent workflows, then inspect usage by model, session, and time range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency resolution for the Node.js package may affect installation integrity. <br>
Mitigation: Review npm dependency resolution before installing or deploying the skill. <br>
Risk: SQLite usage and metadata fields can retain local prompt details, customer data, credentials, or other sensitive context if supplied by the integrator. <br>
Mitigation: Choose the SQLite database path deliberately and avoid storing secrets, full prompts, customer data, or credentials in metadata unless local retention is acceptable. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/imgolye/agent-usage-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite-backed usage records, cost summaries, budget evaluations, and time-series reporting patterns.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

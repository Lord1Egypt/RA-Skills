## Description: <br>
Manage Linear issues, projects, and cycles via GraphQL for backlog triage, task creation, sprint progress checks, and team reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achilles2200ai-sys](https://clawhub.ai/user/achilles2200ai-sys) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, product operators, and team leads use this skill to query and modify Linear work items from an agent workflow. It is suited for creating issues, checking sprint status, searching backlogs, updating priorities or states, adding comments, and producing concise status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live read and write access to Linear workspace data. <br>
Mitigation: Install it only in workspaces where the agent is allowed to access Linear, and require explicit review before create, update, comment, or bulk mutation actions. <br>
Risk: The skill requires a sensitive Linear API key. <br>
Mitigation: Use the least-privileged Linear key available, keep it out of tracked files and shared logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/achilles2200ai-sys/clawbounty-2-linear) <br>
- [Publisher profile](https://clawhub.ai/user/achilles2200ai-sys) <br>
- [Linear GraphQL API endpoint](https://api.linear.app/graphql) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown instructions with inline bash and GraphQL examples; API calls return JSON responses from Linear.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINEAR_API_KEY and local curl and jq for the documented command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, CHANGELOG, effector.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

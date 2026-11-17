## Description:

Automate Nbm provides specialized agent personas and orchestration workflows for routing software, marketing, product, testing, and support tasks through single-agent, department, or multi-agent execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project teams, and operators use Automate Nbm to route GitHub issue or CLI task descriptions to specialized agents, coordinate multi-agent delivery plans, and produce structured task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist an AUTOMATE_SSH_KEY value to ~/.ssh/automate_key.

Mitigation: Use a short-lived deploy key or external ssh-agent handling, and avoid providing AUTOMATE_SSH_KEY on persistent or shared runners unless local key persistence is acceptable.

Risk: Task descriptions and results can be written to predictable local files and sent through GitHub comments or webhook notifications.

Mitigation: Avoid submitting sensitive task content, restrict notification targets, and review result files and outbound notification settings before enabling automation.

Risk: Broad issue labels and keyword-triggered dispatch can route tasks automatically.

Mitigation: Limit task-triggering labels and repository_dispatch senders to trusted repository users, and review automation runs before using the skill in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ironiclawdoctor-design/skills/automate-nbm)
- [Publisher profile](https://clawhub.ai/user/ironiclawdoctor-design)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Agent Registry](AGENTS.md)
- [Agents Orchestrator](orchestrator/SKILL.md)
- [Agency Agents upstream project](https://github.com/msitarzewski/agency-agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and optional JSON result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local task result files and post task updates through configured GitHub or webhook notification targets.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter; package.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

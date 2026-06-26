## Description: <br>
Orchestrates a multi-agent dev or agency team with shared memory, structured handoffs, role templates, and OpenClaw session guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realm1lf](https://clawhub.ai/user/realm1lf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to organize specialized OpenClaw agents across planning, development, QA, security review, customer context, and handoff workflows. It is most useful when a team needs a shared local folder structure for customer tasks, portfolio status, role identities, and multi-agent routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared team folders can accumulate customer context, task details, and operational notes that should not contain credentials. <br>
Mitigation: Choose TEAM_ROOT deliberately, keep passwords and API keys out of Markdown and JSON files, reference secret-manager entry names instead, and use a .gitignore when tracking TEAM_ROOT with Git. <br>
Risk: External chat channels, scheduled work, or multi-agent routing can expand which agents or gateways can act on project files. <br>
Mitigation: Enable those integrations only after reviewing each agent's gateway permissions, sandbox scope, and routing entries in TEAM_ROOT/team/AGENTS.md. <br>
Risk: Agents in separate workspaces or containers may read different paths and create fragmented handoffs. <br>
Mitigation: Use one resolved absolute TEAM_ROOT for all participating agents and mount it at the same path in every sandbox or container that needs access. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Overview](SKILL.md) <br>
- [OpenClaw Team Setup Guide](references/OPENCLAW_TEAM_SETUP_GUIDE.md) <br>
- [First-Time Setup](references/SKILL-SETUP.md) <br>
- [OpenClaw Layout](references/OPENCLAW_LAYOUT.md) <br>
- [Board Schema](references/BOARD_SCHEMA.md) <br>
- [Role Templates](references/ROLE_TEMPLATES.md) <br>
- [Customer Context Template](references/CUSTOMER_CONTEXT.template.md) <br>
- [Structure Map](references/ORG_CHART_EXAMPLE.md) <br>
- [OpenClaw Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent) <br>
- [OpenClaw Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) <br>
- [OpenClaw Multi-Agent Sandbox Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) <br>
- [Upstream Multi-Agent Team Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/multi-agent-team.md) <br>
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with setup prompts, role snippets, JSON schema examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; produces file layout guidance and handoff conventions rather than binaries or secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: metadata.version, CHANGELOG, ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

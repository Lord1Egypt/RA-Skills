## Description:

Zero-knowledge secrets infrastructure for AI agents to manage the credential lifecycle without seeing secret values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steppacodes](https://clawhub.ai/user/steppacodes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use AgentSecrets to let agents manage secret names, sync credential state, and make authenticated API calls through the AgentSecrets CLI or MCP server without exposing plaintext credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad credential automation through an external CLI distribution path.

Mitigation: Install only when the steppacodes publisher and AgentSecrets CLI distribution path are trusted, and prefer pinned, verifiable releases.

Risk: Authenticated outbound calls can expose data if destinations are too broadly authorized.

Mitigation: Keep workspace domain allowlists narrow and review each new destination before allowing calls.

Risk: Environment-variable injection can leak secrets through child process logs, telemetry, dumps, or inherited environments.

Mitigation: Prefer the proxy call or MCP api_call flows for sensitive services, and avoid environment injection unless the child process is trusted.

Risk: Production or global secret changes can affect critical environments.

Mitigation: Require explicit user approval and local password verification before production or global secret creation, modification, deletion, or environment switching.

## Reference(s):

- [AgentSecrets ClawHub Skill Page](https://clawhub.ai/steppacodes/skills/agentsecrets)
- [AgentSecrets Official Website](https://agentsecrets.theseventeen.co)
- [AgentSecrets GitHub Repository](https://github.com/The-17/agentsecrets)
- [AgentSecrets Security Docs](https://github.com/The-17/agentsecrets/blob/main/docs/PROXY.md)
- [AgentSecrets Engineering Blog](https://engineering.theseventeen.co/series/building-agentsecrets)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides CLI and MCP workflow guidance; agents operate on key names and should not output plaintext secret values.]

## Skill Version(s):

1.1.4 (source: server release metadata; artifact frontmatter reports 3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

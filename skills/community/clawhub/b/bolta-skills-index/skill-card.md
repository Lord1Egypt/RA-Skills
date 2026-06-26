## Description: <br>
Bolta Skills Registry - canonical index and orchestration layer for all Bolta skills, organized by plane. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxfritzhand](https://clawhub.ai/user/maxfritzhand) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and workspace operators use this registry skill to discover Bolta skill capabilities, choose install sets, and plan workspace-aware social media automation workflows. It routes users toward the appropriate Bolta skills rather than executing content operations directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Bolta API credentials for related Bolta workflows. <br>
Mitigation: Use environment variables or a secret manager, rotate keys regularly, and never paste or commit API keys. <br>
Risk: Over-broad API keys or agent roles can grant unnecessary content, approval, or team-management authority. <br>
Mitigation: Use the least-privilege Bolta key and role for the intended workspace; avoid editor, admin, and team-management scopes unless required. <br>
Risk: The registry directs users toward external Bolta domains and related repositories. <br>
Mitigation: Install only after confirming trust in the listed Bolta domains and verifying linked repositories before following broader installation steps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maxfritzhand/bolta-skills-index) <br>
- [Bolta API Documentation](https://bolta.ai/docs/api) <br>
- [Bolta MCP Endpoint](https://mcp.bolta.ai/mcp) <br>
- [Bolta Skills Pack](https://github.com/boltaai/bolta-skills) <br>
- [BoltaClaw Self-Hosted Runtime](https://github.com/boltaai/boltaclaw-self-hosted) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with structured recommendations and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Registry index only; it does not directly call APIs or execute content operations.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

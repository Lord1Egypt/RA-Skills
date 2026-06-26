## Description: <br>
Use when designing, reviewing, or refactoring a CLI that must serve AI agents alongside humans, or when converting an API or SDK into an agent-usable CLI interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate, design, and refactor command-line interfaces so they are usable by humans, AI agents, and orchestration systems. It produces structured CLI design reviews, rubric scores, safety guidance, and prioritized refactor plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes authentication and credential-handling examples that could be misunderstood as permission for the agent to own secret retrieval or refresh. <br>
Mitigation: Use the examples as design guidance only: humans or orchestrators should obtain credentials, inject scoped values through trusted environment or config channels, and avoid exposing raw secrets in prompts or logs. <br>
Risk: CLI design recommendations may be applied to mutating or destructive commands without enough runtime safeguards. <br>
Mitigation: Require dry-run previews, explicit safety tiers, stable structured errors, sandbox-aware failure behavior, and human review before implementing destructive actions. <br>
Risk: The artifact includes a notify-only update workflow that can run git commands and pull changes only after user consent. <br>
Mitigation: Prefer ClawHub or a pinned Git revision for installation, review upstream changes before approving any pull, and keep update consent with the human operator. <br>
Risk: This is a third-party release, so trust depends on the publisher and repository rather than NVIDIA ownership. <br>
Mitigation: Install only if the publisher is trusted, review the release evidence and security summary, and scan changes before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/agent-native-design) <br>
- [Agent Native Design Documentation](https://agents365-ai.github.io/agent-native-design/) <br>
- [Design Patterns](references/design-patterns.md) <br>
- [Review Rubric](references/rubric.md) <br>
- [Review Checklists](references/checklists.md) <br>
- [Testing Guidance](references/testing.md) <br>
- [Hybrid MCP and CLI Guidance](references/hybrid-mcp-cli.md) <br>
- [Examples](references/examples.md) <br>
- [Citations](references/citations.md) <br>
- [OpenAI Codex Sidecar Metadata](agents/openai.yaml) <br>
- [Release v1.3.3](https://github.com/Agents365-ai/agent-native-design/releases/tag/v1.3.3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, checklists, JSON examples, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rubric scores, seven-principle reviews, key risks, and prioritized P0/P1/P2 refactor plans.] <br>

## Skill Version(s): <br>
1.3.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Semantic code search and AI-powered codebase Q&A across indexed repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodion-m](https://clawhub.ai/user/rodion-m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover indexed repositories, run semantic code searches, fetch referenced artifacts, and ask codebase questions for onboarding, debugging, dependency exploration, and feature planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote code search and Q&A can expose repository content, prompts, or fetched artifacts to the CodeAlive service. <br>
Mitigation: Install only if you trust CodeAlive and the publisher with repositories available to the configured API key; avoid sending secrets, regulated data, or proprietary code that should not leave the environment. <br>
Risk: API keys may be exposed if pasted into chat or command-line history. <br>
Mitigation: Prefer the interactive setup and OS credential store, and use a scoped key where possible. <br>
Risk: A misconfigured CODEALIVE_BASE_URL could send requests to an unintended service. <br>
Mitigation: Verify CODEALIVE_BASE_URL before use and keep the default service unless a trusted private CodeAlive instance is required. <br>


## Reference(s): <br>
- [Query Patterns](references/query-patterns.md) <br>
- [CodeAlive Workflows](references/workflows.md) <br>
- [CodeAlive MCP Server](https://github.com/CodeAlive-AI/codealive-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with optional JSON output from CLI scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote API calls require a CodeAlive API key and access to the selected indexed data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

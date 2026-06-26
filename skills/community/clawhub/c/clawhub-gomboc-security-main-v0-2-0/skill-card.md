## Description: <br>
Automatically scans codebases for security and configuration issues, generates deterministic fixes, and can apply remediation through CLI, MCP, or CI/CD workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewsweeney](https://clawhub.ai/user/matthewsweeney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan repositories, generate remediation output, and optionally apply fixes to infrastructure, application, and configuration code. It is intended for agent-assisted security remediation workflows where diffs are reviewed before merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate repository changes, commits, and pushes with limited safeguards. <br>
Mitigation: Run remediation on a clean branch, review generated diffs before merge, require PR review, and avoid unattended push workflows. <br>
Risk: The skill requires a Gomboc personal access token for API-backed scanning and remediation. <br>
Mitigation: Use a dedicated least-privilege token supplied through environment variables or CI secrets, and rotate it if exposed. <br>
Risk: The MCP workflow can run a containerized service that interacts with the workspace. <br>
Mitigation: Pin or verify the MCP container image before use and limit workspace access to the minimum required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/matthewsweeney/clawhub-gomboc-security-main-v0-2-0) <br>
- [Setup Guide](references/setup.md) <br>
- [MCP Integration Guide](references/mcp-integration.md) <br>
- [GitHub Actions Integration](references/github-action.md) <br>
- [Security Audit and Practices](SECURITY.md) <br>
- [Gomboc Documentation](https://docs.gomboc.ai) <br>
- [Gomboc Community Edition](https://docs.gomboc.ai/getting-started-ce) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON, SARIF, code snippets, and command-line output depending on the selected workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate repository changes, commits, or pushes when remediation options are explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact documentation reports skill version 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

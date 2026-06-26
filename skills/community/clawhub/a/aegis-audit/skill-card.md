## Description: <br>
Aegis Audit performs behavioral security audits for AI agent skills and MCP tools using deterministic static analysis, cryptographic lockfile generation, and optional LLM-powered intent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanguineseal](https://clawhub.ai/user/sanguineseal) <br>

### License/Terms of Use: <br>
AGPL-3.0 or commercial enterprise license <br>


## Use Case: <br>
Developers, security reviewers, and teams responsible for agent governance use this skill to inspect skills, tools, plugins, or MCP servers before installation or approval. It helps produce line-referenced security reports, risk scoring, capability summaries, and lockfile verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional LLM mode can send scanned code to third-party providers when enabled. <br>
Mitigation: Keep LLM analysis disabled for private or regulated code unless the provider and data handling terms are approved. <br>
Risk: Scanning repositories that contain secrets or credentials can expose sensitive material if optional LLM analysis is enabled. <br>
Mitigation: Run deterministic offline scans with `--no-llm` and avoid scanning secrets or credentials with third-party LLM analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanguineseal/aegis-audit) <br>
- [Aegis project homepage](https://github.com/Aegis-Scan/aegis-scan) <br>
- [Aegis Audit package](https://pypi.org/project/aegis-audit/) <br>
- [Aegis Skill Developer Best Practices](https://github.com/Aegis-Scan/aegis-scan/blob/main/docs/SKILL_DEVELOPER_GUIDE.md) <br>
- [Aegis licensing](https://github.com/Aegis-Scan/aegis-scan/blob/main/aegis-core/LICENSING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON report workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic scans run offline by default; optional LLM analysis requires explicit provider configuration.] <br>

## Skill Version(s): <br>
0.1.10 (source: frontmatter, changelog, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

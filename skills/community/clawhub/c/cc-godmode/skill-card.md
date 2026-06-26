## Description: <br>
Self-orchestrating multi-agent development workflows. You say WHAT, the AI decides HOW. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cubetribe](https://clawhub.ai/user/cubetribe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to orchestrate multi-agent software development workflows, including feature work, bug fixes, API changes, validation, testing, documentation, and release preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent toward broad file writes, shell commands, browser actions, and GitHub operations. <br>
Mitigation: Use it only in trusted repositories and require explicit approval before file writes, shell commands, PR merges, issue closure, releases, tags, CI/CD actions, or production-like operations. <br>
Risk: Runtime workflows may require credentials and network access. <br>
Mitigation: Scope GitHub, Claude, and MCP credentials narrowly and provide only the access needed for the current workflow. <br>
Risk: Browser and screenshot testing can expose sensitive application data. <br>
Mitigation: Avoid live customer data and secret-bearing pages during Playwright, Lighthouse, or screenshot-based testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cubetribe/cc-godmode) <br>
- [Source repository](https://github.com/cubetribe/openclaw-godmode-skill) <br>
- [README](artifact/README.md) <br>
- [Workflow documentation](artifact/docs/WORKFLOWS.md) <br>
- [Agent specifications](artifact/docs/AGENTS.md) <br>
- [Troubleshooting guide](artifact/docs/TROUBLESHOOTING.md) <br>
- [Migration guide](artifact/docs/MIGRATION.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline command examples and agent handoff reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create versioned reports, documentation updates, code changes, tests, screenshots, and release notes depending on the requested workflow.] <br>

## Skill Version(s): <br>
5.11.3 (source: SKILL.md frontmatter, clawdis.yaml, CHANGELOG.md, and server release metadata; released 2026-02-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

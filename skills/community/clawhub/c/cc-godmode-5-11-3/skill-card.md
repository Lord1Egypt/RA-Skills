## Description: <br>
Self-orchestrating multi-agent development workflows. You say WHAT, the AI decides HOW. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongbai233](https://clawhub.ai/user/kongbai233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multi-agent development workflows for features, bug fixes, API changes, research tasks, issue processing, and releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward broad file, shell, browser, web, and GitHub release actions at runtime. <br>
Mitigation: Install only in repositories where that authority is acceptable, limit GitHub and MCP access unless needed, and require explicit human approval before merges, branch deletion, tags, releases, CI/CD changes, or other remote repository mutations. <br>
Risk: Runtime workflows may require credentials, network access, and local binaries. <br>
Mitigation: Use least-privilege tokens, avoid production credentials, and verify the available tools before starting workflows that depend on shell, browser, or GitHub operations. <br>
Risk: Generated reports and screenshots may expose sensitive repository or application data. <br>
Mitigation: Review generated artifacts before sharing them outside the working environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongbai233/cc-godmode-5-11-3) <br>
- [Publisher profile](https://clawhub.ai/user/kongbai233) <br>
- [Project repository listed in artifact metadata](https://github.com/cubetribe/openclaw-godmode-skill) <br>
- [Related original GodMode repository listed in README](https://github.com/cubetribe/ClawdBot-GodMode) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Code](https://claude.ai/code) <br>
- [Workflow documentation](docs/WORKFLOWS.md) <br>
- [Agent documentation](docs/AGENTS.md) <br>
- [Troubleshooting documentation](docs/TROUBLESHOOTING.md) <br>
- [Migration documentation](docs/MIGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, workflow reports, checklists, and implementation handoffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only package; runtime behavior depends on the host agent tools, configured MCP servers, credentials, and local binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata version 5.11.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

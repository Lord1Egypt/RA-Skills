## Description: <br>
AEO analyst orchestration that coordinates canonry sweeps and aeo-audit analysis with persistent user-scoped memory and proactive regression response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arberx](https://clawhub.ai/user/arberx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and developers use Aero to monitor AI answer-engine citation coverage, investigate regressions, generate AEO reports, and plan data-grounded content or site changes. It can also guide approved WordPress and Elementor update workflows when connected to the required MCP tools and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward production WordPress or Elementor edits, including page deletion, content changes, custom CSS, or script insertion. <br>
Mitigation: Use a staging-first workflow, review diffs and visual output, require human approval before production changes, and keep backups or exports before destructive actions. <br>
Risk: The skill may require sensitive credentials for GA4, traffic sources, Canonry, or WordPress MCP connections. <br>
Mitigation: Keep .mcp.json secrets out of source control, use least-privilege staging and production credentials, and rotate credentials if they are exposed. <br>
Risk: Durable memory can drift or retain sensitive project context if used for project-scoped facts. <br>
Mitigation: Store only user-scoped preferences in memory and re-query Canonry for project facts, citation metrics, run history, and client data. <br>
Risk: AEO recommendations can be misleading if citation, traffic, or report data is stale or incomplete. <br>
Mitigation: Confirm recent sync status before quoting analytics, ground claims in Canonry evidence, and avoid promising that fixes will appear in the next sweep. <br>


## Reference(s): <br>
- [Aero ClawHub page](https://clawhub.ai/arberx/aero) <br>
- [Canonry homepage](https://canonry.ai) <br>
- [Aero repository](https://github.com/AINYC/aero) <br>
- [AEO Discovery](references/aeo-discovery.md) <br>
- [Memory Patterns](references/memory-patterns.md) <br>
- [Orchestration Workflows](references/orchestration.md) <br>
- [Regression Playbook](references/regression-playbook.md) <br>
- [Reporting Templates](references/reporting.md) <br>
- [Elementor + WordPress MCP Development Guide](references/wordpress-elementor-mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and code or configuration diffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce report-generation commands, AEO findings, recommended next steps, and proposed WordPress or Elementor changes for human approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Run a two-pass, multidisciplinary code audit led by a tie-breaker lead, combining security, performance, UX, DX, and edge-case analysis into one prioritized report with concrete fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Swader](https://clawhub.ai/user/Swader) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to perform structured code audits across backend, frontend, APIs, infrastructure scripts, and product flows. It produces a risk-ranked review with concrete remediation and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional sync script can overwrite or delete local agent skill directories and does not safely constrain destination names. <br>
Mitigation: Review scripts/sync-to-agents.sh before running it, prefer the default skill name, avoid values containing slashes or '..', and back up existing local agent skill folders before syncing. <br>


## Reference(s): <br>
- [Audit Framework](references/audit-framework.md) <br>
- [Claude Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) <br>
- [Cursor Skills Documentation](https://cursor.com/docs/context/skills) <br>
- [Open Skills Installer](https://github.com/vercel-labs/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with findings, assumptions, remediation summary, and verification checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are prioritized by severity, blast radius, and exploitability, with confidence and evidence references where available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

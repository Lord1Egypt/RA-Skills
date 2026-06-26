## Description: <br>
ClawGuard security assistant for OpenClaw that reads scan reports, explains findings, analyzes fix impact, and guides configuration remediation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r0llcre](https://clawhub.ai/user/r0llcre) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand ClawGuard scan reports for OpenClaw, prioritize security findings, and receive guided remediation steps. It is intended for report analysis, impact review, and configuration-fix guidance rather than performing scans itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guided remediation can change OpenClaw configuration and may affect existing integrations. <br>
Mitigation: Show the proposed diff, require explicit confirmation, create a backup, validate syntax, and advise restart or reload after changes. <br>
Risk: Incomplete or large scan reports can lead to missed context or overlong analysis. <br>
Mitigation: Summarize reports first, use the report parser for large exports, and flag best-effort or unchecked findings as evidence limitations. <br>
Risk: L2 local scan results are sent to ClawGuard for server-side analysis. <br>
Mitigation: Use L1 browser scans when the user wants local-only analysis and disclose the L2 data handling tradeoff before recommending it. <br>


## Reference(s): <br>
- [ClawGuard homepage](https://clawguardsecurity.ai) <br>
- [ClawGuard skill repository](https://github.com/R0llcre/clawguard-skill) <br>
- [Report parsing](references/report-parsing.md) <br>
- [Finding explanations](references/finding-explain.md) <br>
- [Finding catalog](references/finding-catalog.md) <br>
- [Impact analysis](references/impact-analysis.md) <br>
- [Fix procedures](references/fix-procedures.md) <br>
- [Scan guide](references/scan-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, diff blocks, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language; remediation guidance requires user confirmation and backups before configuration changes.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

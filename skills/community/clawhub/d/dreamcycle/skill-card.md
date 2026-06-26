## Description: <br>
AI Agent Self-Reflection Engine: scan session logs, detect failure patterns, analyze recurrence trends, and suggest automated fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qize-auto](https://clawhub.ai/user/qize-auto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use DreamCycle to inspect accumulated AI agent session logs, identify recurring failures and trend changes, and receive suggested fixes for known failure patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs and retained trend history may contain sensitive information. <br>
Mitigation: Run DreamCycle only on log folders intended for analysis, avoid logs containing secrets when possible, and delete ~/.dreamcycle/scan_history.json if local trend history should not be retained. <br>


## Reference(s): <br>
- [DreamCycle homepage](https://github.com/qize-auto/dreamcycle) <br>
- [DreamCycle on ClawHub](https://clawhub.ai/qize-auto/dreamcycle) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown and command-line text, with optional JSON output from the referenced CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes JSON session logs and stores local trend history at ~/.dreamcycle/scan_history.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

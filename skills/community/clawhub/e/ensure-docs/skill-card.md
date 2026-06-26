## Description: <br>
Verify documentation coverage and generate missing docs interactively. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit documentation coverage across Python, TypeScript/JavaScript, and Go projects, identify Diataxis coverage gaps, and optionally generate missing documentation after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit documentation and agent-instruction files when generation is enabled. <br>
Mitigation: Use report-only mode for audit-only reviews, and review proposed documentation, AGENTS.md, CONTRIBUTING.md, or compatibility-symlink changes before accepting them. <br>


## Reference(s): <br>
- [Ensure Docs workflow](references/workflow.md) <br>
- [Diataxis documentation framework](https://diataxis.fr/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with JSON verifier results and optional documentation edits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run language-specific documentation checks and linters when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

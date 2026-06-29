## Description: <br>
Smart text comparison tool with format-aware diffing, AI explanation, and 3-way merge for structured JSON, YAML, CSV, code, and plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare files or directories, inspect structured changes, generate readable diff reports, and prepare three-way merge results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diffs and paste-mode input may contain secrets or proprietary content, and AI explanations may process selected diff hunks. <br>
Mitigation: Compare only files or directories you intentionally choose; use --no-ai-explain and avoid paste mode for secrets or proprietary content when runtime handling is uncertain. <br>
Risk: The release metadata includes crypto, wallet, and sensitive-credential capability labels that the security evidence describes as inconsistent with the artifact behavior. <br>
Mitigation: Treat those labels as metadata noise unless future evidence shows wallet, credential, or crypto behavior. <br>


## Reference(s): <br>
- [Diff Wizard on ClawHub](https://clawhub.ai/harrylabsj/diff-wizard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, unified diff, side-by-side text, Markdown, HTML, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AI explanations, merge conflict suggestions, directory summaries, and optional saved output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script constant) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Measures cyclomatic, cognitive, and structural complexity for Python, JavaScript/TypeScript, and Go code with configurable thresholds and text, JSON, or Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local code complexity analysis, identify high-complexity functions, review refactoring candidates, and generate reports or CI quality-gate output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer reads source files from every selected file or directory path, so broad private directories can expose more source content in reports than intended.

Mitigation: Run it only on intended project paths and use exclusions for directories that should not be analyzed.

Risk: Complexity reports may be used as CI quality gates and can fail builds when thresholds are exceeded.

Mitigation: Set project-appropriate thresholds and review reported violations before treating them as release blockers.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text, JSON, or Markdown complexity reports, often accompanied by shell commands to run the analyzer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-selected local files or directories and exits nonzero when configured complexity thresholds are exceeded.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

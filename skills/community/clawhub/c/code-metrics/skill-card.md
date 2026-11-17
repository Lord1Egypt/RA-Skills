## Description:

Analyze code quality metrics across source code, including lines of code by language, comment ratios, function and class counts, largest files, and Python cyclomatic complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect codebases for size, documentation density, function and class counts, largest files, and Python complexity hotspots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer reads source files under the project path supplied by the user and may include project structure and code-derived metrics in its output.

Mitigation: Run it only on repositories intended for inspection, and avoid broad home or system directories when those files should not be included in metrics output.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain-text report or JSON metrics data, with shell command examples for running the analyzer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-language line counts, comment ratio, function and class counts, largest files, and optional Python cyclomatic complexity warnings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

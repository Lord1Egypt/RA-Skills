## Description:

Analyze project metrics including lines of code, language distribution, function complexity, code-to-comment ratio, test coverage indicators, dependency counts, largest files, and tech debt signals across 40+ languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a local codebase and produce project health metrics such as LOC, language distribution, simplified function complexity, dependency counts, test file indicators, largest files, and TODO/FIXME/HACK signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads source files in the target project to compute metrics.

Mitigation: Run it only on codebases the local agent is allowed to inspect, and pass a specific path when scope should be limited.

Risk: Large or broad scans may inspect more files than intended.

Mitigation: Use --language or --max-files to narrow the scan when tighter scope is needed.

Risk: The skill can write a report file when --output is provided.

Mitigation: Choose an explicit output path and review generated reports before sharing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Terminal text, Markdown report, or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a user-requested report file with --output; supports path, language, format, and max-files options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

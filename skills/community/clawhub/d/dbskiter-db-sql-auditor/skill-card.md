## Description:

SQL全生命周期审核，支持SQL规范审核、性能评估、DDL影响分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to audit SQL and DDL with dbskiter, including standards checks, performance review, DDL impact analysis, rule lookup, optimization suggestions, index recommendations, execution-plan analysis, cost estimates, and SQL rewrites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run shell-style dbskiter commands containing user-provided SQL, DDL, database names, and file paths.

Mitigation: Require shell-safe execution that passes SQL, DDL, database names, and file paths as separate validated arguments instead of interpolating them into command strings.

Risk: SQL text, DDL, file paths, or database artifacts may contain secrets or confidential database information.

Mitigation: Use the skill only in environments where dbskiter is trusted, and avoid submitting secrets or confidential artifacts unless the user understands how dbskiter processes them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-sql-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with dbskiter shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include audit scores, issue lists, repair suggestions, DDL impact notes, optimization guidance, index recommendations, execution-plan analysis, cost estimates, and SQL rewrite suggestions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

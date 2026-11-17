## Description:

Formats SQL queries with uppercase keywords, consistent indentation, aligned clauses, and preserved string literals; it does not parse or execute SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to format raw SQL, standardize team SQL style, and prepare queries for review without parsing or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented CLI examples may not match the packaged implementation; security guidance notes that the advertised --indent example is not implemented.

Mitigation: Verify commands against the packaged CLI before use and prefer supported inline SQL or --file invocation paths.

Risk: The formatter is not a SQL parser or syntax validator and may produce unsuitable formatting for unsupported SQL patterns.

Mitigation: Review formatted output before use and rely on a SQL parser, database EXPLAIN, or project-specific validation when correctness matters.

Risk: The manifest may be stale relative to the server file hash evidence.

Mitigation: Use the server-provided file hashes and release fingerprint as the authoritative package integrity evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-sql-formatter)
- [Publisher profile](https://clawhub.ai/user/kofna3369)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Formatted SQL text, Markdown guidance, and inline shell or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local deterministic formatter; no LLM use, SQL parsing, or SQL execution.]

## Skill Version(s):

0.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

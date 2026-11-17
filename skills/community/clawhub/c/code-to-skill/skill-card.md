## Description:

Converts building-code and regulation PDFs into queryable agent skills that index clauses by trigger conditions, preserve mandatory-force wording, extract tables as JSON, and map cross-references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[51comic](https://clawhub.ai/user/51comic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical reviewers use this skill to convert provided building-code or regulation PDFs into structured skills for clause lookup, table lookup, and cross-reference review. It is a retrieval aid and does not replace professional legal, architectural, or engineering judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent, agent-loadable skills from untrusted regulation PDFs.

Mitigation: Run it in an isolated workspace and manually review generated clauses, tables, and index files before loading or publishing them.

Risk: Optional dependency installation can change the host Python environment.

Mitigation: Use a virtual environment, prefer --install-missing ask or no, and install dependencies manually when possible.

Risk: The bundled safety scan may not cover every generated file that this workflow produces.

Mitigation: Treat the scanner as advisory and perform human review of generated clauses, tables, cross-references, and mandatory-force mappings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/51comic/skills/code-to-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/51comic)
- [Artifact reference index](artifact/references/REFERENCES.md)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated skill files, including Markdown clauses, JSON tables, index files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs depend on the supplied PDF and should be reviewed before loading or publishing as an agent skill.]

## Skill Version(s):

1.0.6 (source: server release, SKILL.md frontmatter, _meta.json, CHANGELOG released 2026-08-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Analyzes Vue, React, and Angular front-end trading code to derive business requirements and build a reusable trading knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshphe](https://clawhub.ai/user/joshphe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect existing trading-domain front-end code, extract UI structure, APIs, business rules, and produce reverse-engineered requirements for review, refactoring, or knowledge management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cache and knowledge graph files may retain source-derived analysis data.

Mitigation: Use the skill only on code you are comfortable storing locally, set cache and knowledge paths deliberately, and clear or disable cache for sensitive analysis.

Risk: The bundled repair script can overwrite React and Angular parser implementations.

Mitigation: Do not run fix_setup.sh unless the skill directory is backed up and overwriting those parser files is acceptable.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Install in a virtual environment and pin dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joshphe/skills/code-to-requirement-analyser)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON analysis results, optional Markdown reports, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write parser cache entries, knowledge graph JSON files, and user-selected report or output files.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

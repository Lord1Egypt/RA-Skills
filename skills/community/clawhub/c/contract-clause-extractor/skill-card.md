## Description:

Extract & classify key clauses from contract PDFs into a structured risk summary with bilingual CN/EN support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal operations teams use this skill to extract contract clauses, classify them into standard categories, compare contract versions, and produce bilingual risk summaries for review. Its outputs should support triage and discussion, not replace qualified legal counsel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that the script can produce canned legal-risk conclusions without actually reading contract content.

Mitigation: Treat results as triage only; verify every extracted clause and risk rating against the source contract with a real parser, reviewer, and qualified legal counsel.

Risk: Automated summaries and negotiation suggestions can be mistaken for legal advice.

Mitigation: Include the legal-review disclaimer in user-facing outputs and require qualified counsel before contractual decisions.

Risk: Contracts may contain confidential or personal information.

Mitigation: Avoid storing source documents or sensitive identifiers in generated summaries unless the user explicitly requests it and the handling environment is appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/contract-clause-extractor)
- [Contract Clause Risk Categories](references/risk-categories.json)
- [Input schema](schemas/input.schema.json)
- [Output schema](schemas/output.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, structured JSON, comparison tables, bilingual extraction tables, and CLI command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include clause categories, risk levels, hidden-risk alerts, modification suggestions, glossary entries, and legal-review disclaimers.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

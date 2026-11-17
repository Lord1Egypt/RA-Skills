## Description:

DeepLegal Chinese Contract helps agents draft, review, negotiate, and assess contracts across PRC, US, and Hong Kong contexts, including Chinese, English, and bilingual agreements with case-aware legal reasoning and DOCX review output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hekuangviolet-ai](https://clawhub.ai/user/hekuangviolet-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal operations teams use this skill to review, draft, and negotiate Chinese, cross-border, and offshore contracts with practical legal risk assessment. The skill can produce contract review markup, clean drafts, negotiation positions, and concise supporting summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contracts and generated JSON or DOCX files may contain confidential deal terms or legal positions.

Mitigation: Use an isolated environment for sensitive matters, limit access to generated files, and delete temporary input files after document generation.

Risk: Legal outputs may be incomplete, jurisdiction-specific, or unsuitable for reliance without professional review.

Mitigation: Have qualified counsel verify legal analysis, clause language, and final documents before using them in business decisions or negotiations.

Risk: The DOCX generator depends on Python packages that must be installed in the execution environment.

Mitigation: Pin and audit the Python dependencies before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hekuangviolet-ai/skills/deeplegal)
- [Legal Reference - Jurisdiction Guide](artifact/legal-reference.md)
- [Key Litigation Cases & Judicial Precedents](artifact/litigation-cases.md)
- [Standard Contract Clauses Reference](artifact/contract-clauses.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance, JSON document-generation input, shell commands, and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON and DOCX files containing contract text, legal comments, and deal terms.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

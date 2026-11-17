## Description:

Format, audit, and polish academic references in APA 7th style, including in-text citations, DOI/URL cleanup, and correction tables for student papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mia956](https://clawhub.ai/user/mia956)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and academic writers use this skill to format APA 7 reference lists, audit incomplete citation metadata, clean DOI/URL and author formatting, and prepare in-text citation examples. It supports bilingual workflows where corrections can be explained in Chinese while English APA 7 references are produced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Python checker is a quick heuristic and can miss APA 7 issues or flag acceptable references.

Mitigation: Use checker output only as triage, then manually apply the APA 7 rules and citation-integrity guidance in the skill instructions.

Risk: The smoke test writes to a fixed temporary path and is not appropriate for elevated-privilege execution as-is.

Mitigation: Run the smoke test without elevated privileges or fix its temporary-file handling before using it in privileged automation.

Risk: Incomplete citation metadata could lead to unsupported reference details if handled carelessly.

Mitigation: Mark missing authors, years, publication data, DOIs, and URLs explicitly, and verify external identifiers before claiming they exist.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Demo references](artifact/examples/demo_references.txt)
- [ClawHub skill page](https://clawhub.ai/mia956/skills/apa7-reference-helper-mia956)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown with reference lists, compact correction tables, citation examples, missing-metadata markers, and optional shell commands for the local checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese correction explanations while preserving English APA 7 reference entries; the helper script can emit readable text or JSON audit results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

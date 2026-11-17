## Description:

Verify and normalize biomedical and life-science reference lists, with a focus on AI-caused citation errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emp-tca](https://clawhub.ai/user/emp-tca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check biomedical and life-science reference lists for DOI, PMID, title, author, journal, year, and metadata inconsistencies, then produce reviewable reports and normalized citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification runs may contact Crossref, PubMed/NCBI, and OpenAlex with public identifiers and sometimes citation titles.

Mitigation: Use format-only mode or disable providers for confidential drafts or unpublished research topics; provide contact email or API keys only when intentionally sending them to providers.

Risk: Formatting-only output does not establish reference authenticity.

Mitigation: Use the verification pipeline before treating references as usable, and review the generated reports and evidence links for unresolved or blocked records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emp-tca/skills/biomedical-reference-verifier)
- [README](README.md)
- [Verification Policy](references/verification_policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, self-contained HTML report, JSON audit/index artifacts, fixed reference Markdown, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report files and never overwrites the source document; format-only mode is offline, while verification may contact Crossref, PubMed/NCBI, and OpenAlex.]

## Skill Version(s):

1.2.1 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

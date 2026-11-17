## Description:

Verify a BibTeX file for hallucinated or fabricated references by cross-checking every entry against CrossRef, arXiv, and DBLP, reporting each reference as verified, suspect, or not found with field-level mismatch details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloml0326](https://clawhub.ai/user/helloml0326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, reviewers, and authors use this skill to audit BibTeX bibliographies for fabricated, hallucinated, or incorrectly cited references before publication or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bibliography verification may send citation metadata to CrossRef, arXiv, and DBLP.

Mitigation: Do not run network verification on private, unpublished, or regulated bibliography data unless sharing citation metadata with those services is acceptable.

Risk: The skill requires installing dependencies before use.

Mitigation: Install in a virtual environment and consider pinning or reviewing dependencies first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloml0326/skills/bib-verify)
- [Publisher profile](https://clawhub.ai/user/helloml0326)
- [Full pipeline options](../paper-review/reference.md)
- [Combined PDF review and BibTeX verification](../paper-review/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and tabular status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports BibTeX entries as verified, suspect, or not_found, with field-level mismatch details for titles, authors, years, and DOIs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

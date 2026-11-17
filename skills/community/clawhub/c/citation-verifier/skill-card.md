## Description:

Verify, normalize, and enrich a single citation or paper identifier. Use when the user pastes a DOI, URL, arXiv ID, PubMed ID, citation string, or paper title and wants it checked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papersareflowing](https://clawhub.ai/user/papersareflowing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to verify and normalize a known academic citation or paper identifier, then receive a concise structured record and next-step guidance when verification is ambiguous or fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misapplied to broad literature searches or paper recommendations, which are outside its intended scope.

Mitigation: Use it only for a specific known citation, DOI, URL, arXiv ID, PubMed ID, citation string, or paper title.

Risk: Ambiguous or failed citation matches may be mistaken for verified paper records.

Mitigation: Preserve the verification status in the output and ask for a more complete title or a different identifier when the match is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/papersareflowing/skills/citation-verifier)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes title, authors, year, venue, DOI, additional identifiers, and verification status when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Checks references against GB/T 7714—2025 and verifies eligible citations against public bibliographic records, with manual-check guidance where automated verification is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libv70](https://clawhub.ai/user/libv70)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, editors, and students use this skill to review reference lists and in-text citations for GB/T 7714—2025 formatting, check eligible records against bibliographic databases, and receive corrected examples and manual verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live verification may disclose citation metadata from confidential or embargoed reference lists to public bibliographic services.

Mitigation: Use manual or offline review for sensitive material unless sharing citation metadata with Crossref or OpenAlex is acceptable.

Risk: A missing database match may be mistaken for proof that a citation does not exist.

Mitigation: Treat inconclusive matches as unverified and follow the manual-check guidance before making an existence claim.

## Reference(s):

- [GB/T 7714—2025 formatting rules](artifact/references/gbt7714-2025-rules.md)
- [Citation verification sources and methods](artifact/references/verification-sources.md)
- [Crossref works API](https://api.crossref.org/works)
- [OpenAlex works API](https://api.openalex.org/works)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reference-check report with corrected citation examples and manual verification checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-entry formatting findings, evidence-based verification status, and suggested corrections.]

## Skill Version(s):

4.0.5 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

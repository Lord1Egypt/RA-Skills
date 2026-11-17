## Description:

Searches academic literature for missing ChatMOSP MSR/KMC parameters and returns extracted, validated parameter tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanyangye](https://clawhub.ai/user/sanyangye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers using ChatMOSP use this skill when the MOSP database lacks required parameters. It searches academic sources and supplementary information, extracts surface energy, adsorption energy, and interaction matrix values, then returns a scored table for user review and handoff to parameter-builder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use browser, web, PDF, and file-reading tools to inspect papers and save supplementary PDFs or text locally.

Mitigation: Install only when this access pattern is acceptable; prefer open-access sources and avoid private logged-in journal sessions unless intended.

Risk: Extracted scientific parameters can be incomplete, unsuitable, or require format conversion before downstream ChatMOSP use.

Mitigation: Review DOI/title/author provenance, completeness scores, reasonability checks, and missing-parameter notes before passing results to downstream skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanyangye/skills/chatmosp-literature-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown responses with JSON-style parameter tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes article title, DOI, authors, parameter values, completeness score, missing-parameter notes, and user confirmation choices.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Verify, repair, explain, and generate BibTeX references with Bibverify's DOI-first CLI and MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hylouis233](https://clawhub.ai/user/hylouis233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use Bibverify to verify and repair BibTeX files, generate entries from DOIs, and explain source-ranking or field-level differences for citation metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required bibverify CLI package may be confused with another package or installed into an unsuitable environment.

Mitigation: Before installing, verify that bibverify is the intended package and consider installing it in a virtual environment.

Risk: Citation repair workflows can modify bibliographic data or create replacement files that users may mistake for final authoritative output.

Mitigation: Do not silently overwrite the source .bib file; explain generated backup, updated, and problem-entry files and call out entries that need manual review.

Risk: Bibliographic lookup sources can disagree or lack complete metadata.

Mitigation: Use Bibverify results as the evidence source, avoid inventing missing metadata, and explain uncertainty when sources disagree.

## Reference(s):

- [Bibverify ClawHub skill page](https://clawhub.ai/hylouis233/skills/bibverify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional inline BibTeX, JSON configuration, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated backup, updated, and problem-entry files created by Bibverify; the skill should not silently overwrite source .bib files.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

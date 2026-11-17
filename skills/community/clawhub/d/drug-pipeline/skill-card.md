## Description:

Searches a pharmaceutical drug database for pipeline and development information by converting natural-language drug questions into structured API queries and returning matching records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombert](https://clawhub.ai/user/bombert)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to look up drug pipeline records by drug name, target, indication, sponsor, modality, phase, route of administration, or development progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drug-search parameters and the NOAH_API_TOKEN are sent to NoahAI's API.

Mitigation: Install only when that data transfer is acceptable, keep the token in the environment rather than chat or command text, and use a controlled Python environment.

Risk: The script can write results to a user-selected path with --output.

Mitigation: Use --output only for paths that are intended to be created or overwritten.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombert/skills/drug-pipeline)
- [NoahAI](https://noah.bio)
- [NoahAI drug search API endpoint](https://www.noah.bio/api/skills/drug_search/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Human-readable text summaries by default, with raw JSON available via the script's --raw option.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOAH_API_TOKEN; script queries can be supplied inline or through a JSON parameters file, and --output can save results to a chosen file path.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

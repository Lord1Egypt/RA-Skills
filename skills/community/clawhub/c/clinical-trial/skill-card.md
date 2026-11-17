## Description:

Searches clinical trial databases by turning natural language questions into structured queries and returning matching trial records from NoahAI clinical trial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombert](https://clawhub.ai/user/bombert)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search clinical trial records by NCT ID, sponsor, indication, phase, drug name, drug modality, target, location, and result availability, then review matching trial summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical-trial search terms and the NOAH_API_TOKEN are sent to Noah's API.

Mitigation: Use a dedicated token, keep it in the environment, and install only where sending these search terms to Noah's API is acceptable.

Risk: Queries could include personal health details.

Mitigation: Avoid entering personal health information or other sensitive personal data in clinical-trial search queries.

Risk: The optional output path can overwrite files accessible to the running user.

Mitigation: Review the target path before using file output and run the skill from an isolated working directory when possible.

Risk: Runtime behavior depends on a Python environment, the requests package, network access, and a valid Noah API token.

Mitigation: Install dependencies in an isolated environment and verify NOAH_API_TOKEN is scoped appropriately before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombert/skills/clinical-trial)
- [NoahAI website](https://noah.bio)
- [NoahAI clinical trial API endpoint](https://www.noah.bio/api/skills/clinical_trial_search/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or text summaries, with optional raw JSON API responses and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOAH_API_TOKEN; optional output paths can write result text to files selected by the user.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

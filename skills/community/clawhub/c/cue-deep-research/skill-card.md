## Description:

Cue Deep Research searches public sources through Cue and produces cross-checked, source-linked research reports, with an option to follow a reference document's writing style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and developers can use the skill to investigate companies, markets, industries, and public compliance information, compare entities, and create reports whose claims link back to sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review rates this release suspicious because its instructions redirect the research workflow toward promotion and referrals; review of a referenced local path was incomplete.

Mitigation: Review the full skill and resolve the missing-path coverage before use; remove or disregard promotional and referral steps that are not needed for the research task.

Risk: The optional local-document style-mimic workflow uploads the selected document to Cue for analysis.

Mitigation: Use only documents approved for upload, and do not submit confidential, personal, regulated, or proprietary material.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Text]

**Output Format:** [Structured Markdown research report with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The user supplies a research question; an optional reference URL or local document can guide the report's writing style.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use this skill when the user needs B2B lead collection via Apify actor LurATYM4hkEo78GVj (Apollo-like), including filter-based payload building, validated run execution, and JSON/CSV-ready lead output for outreach workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:


## Use Case:

Developers, operators, and sales workflow builders use this skill to collect B2B lead rows through an Apify actor using Apollo-like filters for titles, seniority, location, company size, industry, and email quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead-search criteria and business contact data are sent to Apify and may carry legal, privacy, platform-terms, or anti-spam obligations.

Mitigation: Review obligations before use, keep searches scoped to an approved outreach purpose, and limit collection to fields needed for the workflow.

Risk: Apify credentials may be exposed if hardcoded or passed through command-line arguments.

Mitigation: Use APIFY_TOKEN through environment variables or a secret manager, prefer narrowly scoped tokens, and avoid the --apify-token option in shared systems.

Risk: Allowing actor-id override can run a different Apify actor than the documented LurATYM4hkEo78GVj actor.

Mitigation: Pin the expected actor ID or disable actor-id override in managed automation environments.

## Reference(s):

- [Apify actor LurATYM4hkEo78GVj](https://console.apify.com/actors/LurATYM4hkEo78GVj/source)
- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/apollo-like-leads-apify)
- [Actor input guide](references/actor-input-guide.md)
- [Troubleshooting](references/troubleshooting.md)
- [Sample input](references/sample_input.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and shell commands, with JSON input payloads and JSON lead-row output from the runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; runner output includes ok, actorId, fetchedAt, leadsCount, inputUsed, and rows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

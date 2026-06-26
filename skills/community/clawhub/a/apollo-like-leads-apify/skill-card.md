## Description: <br>
Use this skill when the user needs B2B lead collection via Apify actor LurATYM4hkEo78GVj (Apollo-like), including filter-based payload building, validated run execution, and JSON/CSV-ready lead output for outreach workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to build Apollo-like B2B lead payloads, run the Apify actor, and return normalized lead rows for outreach, n8n, Sheets, CSV, or CRM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk collection and export of business contact details can create privacy, anti-spam, platform-terms, and data-retention risk. <br>
Mitigation: Use only contacts you are authorized to process, comply with privacy and anti-spam laws and platform terms, keep result counts limited, leave phone collection off unless necessary, and control where exported lead data is stored and retained. <br>
Risk: The skill requires an Apify token for actor execution. <br>
Mitigation: Use APIFY_TOKEN from the environment or secure runtime configuration, prefer scoped tokens, and avoid hardcoding credentials in workflow templates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/apollo-like-leads-apify) <br>
- [Apify actor source](https://console.apify.com/actors/LurATYM4hkEo78GVj/source) <br>
- [Actor input guide](references/actor-input-guide.md) <br>
- [Sample input](references/sample_input.json) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions and JSON runner output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN; returns ok, actorId, fetchedAt, leadsCount, inputUsed, and rows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

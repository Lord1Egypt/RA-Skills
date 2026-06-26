## Description: <br>
Build targeted company lists for outbound campaigns using Extruct by guiding lookalike, semantic, and deep-search list-building workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkid18](https://clawhub.ai/user/zkid18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and GTM teams use this skill to turn ICP context, seed companies, and campaign goals into targeted company lists for outbound campaigns. The workflow helps choose between lookalike search, broad semantic search, deep qualified search, and table upload through Extruct. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on a separate extruct-api skill and may send company context, seed domains, CSVs, and search results to Extruct. <br>
Mitigation: Before use, verify that the extruct-api skill is trusted and confirm the approved data sources, upload destination, search scope, and result size. <br>
Risk: Outbound lists can include existing customers, partners, competitors, or other do-not-contact domains if exclusions are incomplete. <br>
Mitigation: Review the company context and DNC sources before upload, remove excluded domains during deduplication, and ask the user before skipping missing DNC data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkid18/extruct-list-building) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with query plans, workflow steps, and output preference prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Extruct table links, local CSV guidance, or both after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Searches a pharmaceutical drug database for pipeline and development information by translating drug, target, indication, company, modality, phase, and route questions into structured API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombert](https://clawhub.ai/user/bombert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to turn natural-language pharmaceutical pipeline questions into structured NOAH-backed searches and readable drug development records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pharmaceutical or company research queries to an external NOAH-backed service using NOAH_API_TOKEN. <br>
Mitigation: Set NOAH_API_TOKEN only when you intend to use that service, avoid confidential prompts and parameter files, and install the skill only if you trust the provider and data flow. <br>
Risk: The external service and token permissions are not fully described by the artifact. <br>
Mitigation: Review the service terms, token scope, and organizational approval requirements before deployment. <br>
Risk: Structured query values must match exact API-supported formats, which can produce incomplete or misleading results when mapped incorrectly. <br>
Mitigation: Review generated query parameters, use the documented fallback search strategies, and validate important results against authoritative sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bombert/drug-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/bombert) <br>
- [NOAH website](https://noah.bio) <br>
- [NOAH API endpoint](https://www.noah.bio/api/skills/drug_search/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summaries, with optional raw JSON from the search script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include formatted drug records, total match counts, query guidance, and fallback search strategies.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

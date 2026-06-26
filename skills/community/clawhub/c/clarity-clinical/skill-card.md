## Description: <br>
Clarity Clinical queries clinical variant annotations from ClinVar and population frequency data from gnomAD through Clarity Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and clinical data reviewers use this skill to query gene or HGVS variant records for ClinVar significance, review status, and gnomAD population frequency via Clarity Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and API-authenticated requests are sent to clarityprotocol.io. <br>
Mitigation: Confirm the service is trusted before installation and use only the intended CLARITY_API_KEY environment variable for API credentials. <br>
Risk: Clinical variant data may be mistaken for medical advice. <br>
Mitigation: Treat returned ClinVar and gnomAD information as reference data that requires appropriate clinical review before decision-making. <br>


## Reference(s): <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/clarityprotocol/clarity-clinical) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output is JSON or readable text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to clarityprotocol.io; optional CLARITY_API_KEY raises rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

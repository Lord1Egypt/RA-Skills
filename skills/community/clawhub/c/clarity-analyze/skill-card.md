## Description: <br>
Submit research questions for AI-powered analysis via Clarity Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to submit protein variant and mutation research questions to Clarity Protocol and receive AI analysis grounded in aggregated biomedical data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research questions, variant IDs, focus terms, and additional context are sent to clarityprotocol.io for server-side AI analysis. <br>
Mitigation: Submit only data approved for external processing, and avoid confidential or unpublished research unless that sharing is authorized. <br>
Risk: The skill requires a Clarity write API key for analysis requests. <br>
Mitigation: Use a dedicated CLARITY_WRITE_API_KEY environment variable where possible and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [Clarity Analyze on ClawHub](https://clawhub.ai/clarityprotocol/clarity-analyze) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, guidance] <br>
**Output Format:** [JSON, plain text, or terminal-formatted summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLARITY_WRITE_API_KEY; sends questions and optional variant context to clarityprotocol.io; limited to 10 analysis requests per API key per day.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

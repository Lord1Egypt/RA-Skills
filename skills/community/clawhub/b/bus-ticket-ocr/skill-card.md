## Description: <br>
Recognizes bus ticket documents and returns structured OCR data for key ticket fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to send a local bus ticket image or PDF to the Scnet OCR API and extract structured fields such as ticket number, travel date, stations, fare, and passenger name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticket images are sent to the Scnet OCR API for processing. <br>
Mitigation: Use the skill only for ticket images that are acceptable to process with Scnet, and avoid highly sensitive files when local-only OCR is required. <br>
Risk: The skill requires a sensitive SCNET_API_KEY credential. <br>
Mitigation: Store a dedicated key in an environment variable or config/.env with restrictive permissions, and do not paste the key into chat. <br>
Risk: Server evidence says import provenance is unavailable and security guidance notes unfinished README and homepage metadata. <br>
Mitigation: Verify the publisher profile and release provenance before deploying in environments that require provenance controls. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API Documentation](references/api-docs.md) <br>
- [Bus Ticket Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [Scnet OCR API base](https://api.scnet.cn/api/llm/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON written to standard output, with human-readable error guidance on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and sends the selected ticket file to the Scnet OCR API.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

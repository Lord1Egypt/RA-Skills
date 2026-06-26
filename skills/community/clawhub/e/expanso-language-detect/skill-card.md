## Description: <br>
Detects the language of input text using AI through Expanso Edge CLI or HTTP pipeline modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to identify the language of supplied text and receive a language name, ISO 639-1 code, and confidence score. It can be run as a one-off CLI pipeline or exposed as an HTTP detection endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP/HTTP mode can expose an unauthenticated detection endpoint. <br>
Mitigation: Bind the service to localhost or protect it with firewall and authentication controls before use. <br>
Risk: Submitted text is sent to OpenAI when the OpenAI-backed pipeline is used. <br>
Mitigation: Avoid confidential, regulated, or secret-containing text unless OpenAI processing is approved for that data. <br>
Risk: The pipeline uses the user's OpenAI API key for submitted requests. <br>
Mitigation: Use a restricted or low-quota API key and prefer CLI mode for controlled one-off checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aronchick/expanso-language-detect) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [skill.yaml](skill.yaml) <br>
- [pipeline-cli.yaml](pipeline-cli.yaml) <br>
- [pipeline-mcp.yaml](pipeline-mcp.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis] <br>
**Output Format:** [JSON object with language, code, confidence, and metadata fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI pipeline writes a JSON object to stdout; the HTTP pipeline returns the JSON object as the synchronous response.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

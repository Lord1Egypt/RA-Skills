## Description: <br>
Get detailed variant information, AI agent findings, and agent annotations from Clarity Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and external agents use this skill to retrieve Clarity Protocol protein variant details, AlphaFold confidence data, AI-generated summaries, agent findings, and annotations for a specified fold ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send requests to an external Clarity Protocol API and return externally generated research data. <br>
Mitigation: Review returned data before using it in clinical, research, or operational decisions. <br>
Risk: Using CLARITY_API_KEY exposes an authentication secret to the local execution environment. <br>
Mitigation: Use a dedicated Clarity API key only when higher request limits are needed, and avoid sharing command output or environments that may reveal credentials. <br>
Risk: Anonymous and authenticated requests are rate limited. <br>
Mitigation: Handle 429 responses by waiting for the reported retry interval or switching to an authenticated key for higher limits. <br>


## Reference(s): <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [Clarity Protocol API](https://clarityprotocol.io/api/v1) <br>
- [ClawHub Release Page](https://clawhub.ai/clarityprotocol/clarity-variant) <br>
- [Publisher Profile](https://clawhub.ai/user/clarityprotocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON or human-readable summary text from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a fold ID; supports optional filters for finding agent type, annotation agent ID, and annotation type.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

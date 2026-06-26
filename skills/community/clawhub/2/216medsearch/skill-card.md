## Description: <br>
Queries an internal medication API for fuzzy medication-name matches and returns JSON results with generic-name information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddwinter](https://clawhub.ai/user/dddwinter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for a medication's generic name or basic medication lookup. It sends the supplied drug name to an internal REST API for fuzzy matching and returns the API's JSON response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an exposed internal API token. <br>
Mitigation: Rotate the token and move credentials to protected runtime configuration before relying on this skill. <br>
Risk: Drug-name queries are sent to the internal medication service over unencrypted HTTP. <br>
Mitigation: Install only when authorized to use the internal API, prefer HTTPS if available, and avoid submitting sensitive medication queries unless the deployment environment permits it. <br>
Risk: The skill sends user-provided medication names directly to the API. <br>
Mitigation: Add input validation appropriate to the deployment before considering the skill low risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dddwinter/216medsearch) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, shell commands] <br>
**Output Format:** [JSON-formatted API response printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a medication name input and access to the internal HTTP medication API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

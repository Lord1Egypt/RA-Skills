## Description: <br>
Calls the Agnes AI API to generate images or videos from user prompts using an AGNES_API_KEY credential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Agnes AI images or short videos from confirmed prompts, configure AGNES_API_KEY, and retrieve generated media URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation requests are sent to the external Agnes AI service under the user's API key. <br>
Mitigation: Avoid secrets or personal data in prompts and review Agnes AI terms before use. <br>
Risk: The setup guidance stores AGNES_API_KEY persistently in a shell profile. <br>
Mitigation: Store only the intended key, restrict access to the profile, and remove or rotate the key when it is no longer needed. <br>
Risk: Video generation uses repeated polling against an external task endpoint. <br>
Mitigation: Poll at the documented interval and stop when the task reaches a completed or failed status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/agnespaint) <br>
- [Agnes AI platform](https://platform.agnes-ai.com/) <br>
- [API reference](modules/01-api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown text with curl examples and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNES_API_KEY; image requests return a URL, and video requests poll until completion before returning a URL.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generate PPT/slides with Felo PPT Task API in Claude Code, including API key checks, task creation, polling, and final slide URL output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[comman-kaide](https://clawhub.ai/user/comman-kaide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to create presentation decks from a topic, outline, or notes and receive a generated PPT or live-doc link from Felo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide prompts and any included presentation content are sent to Felo's external service under the user's Felo API key. <br>
Mitigation: Avoid confidential or regulated material unless Felo's terms and data handling are acceptable for the use case. <br>
Risk: The helper script supports FELO_API_BASE, so a misconfigured environment could send prompts and API credentials to an unexpected endpoint. <br>
Mitigation: Confirm FELO_API_BASE is unset or points to the expected Felo OpenAPI host before running the skill. <br>
Risk: The skill requires a Felo API key and may fail when the key is missing, invalid, or revoked. <br>
Mitigation: Set FELO_API_KEY only in the active execution environment and rotate or revoke it according to the user's credential policy. <br>


## Reference(s): <br>
- [Felo PPT Task API](https://openapi.felo.ai/docs/api-reference/v2/ppt-tasks.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>
- [ClawHub Release Page](https://clawhub.ai/comman-kaide/comman-felo-slides) <br>
- [Publisher Profile](https://clawhub.ai/user/comman-kaide) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown result or plain slide URL, with optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status, PPT URL, live document URL, and optional task metadata when JSON output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

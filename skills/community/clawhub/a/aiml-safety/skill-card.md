## Description: <br>
Content moderation and safety checks that classify text or images as safe or unsafe using AI guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimlapihello](https://clawhub.ai/user/aimlapihello) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to check user input or chatbot responses for safety before continuing a workflow or publishing content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content submitted for safety checks is sent to AIMLAPI, which may expose sensitive, private, or regulated data to a third-party service. <br>
Mitigation: Use only with content permitted by the user's AIMLAPI terms and data-handling requirements, and avoid submitting secrets or regulated personal data. <br>


## Reference(s): <br>
- [AIMLAPI Safety API Reference](references/safety-categories.md) <br>
- [AIMLAPI chat completions endpoint](https://api.aimlapi.com/v1/chat/completions) <br>
- [ClawHub skill page](https://clawhub.ai/aimlapihello/aiml-safety) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with optional JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY and sends checked content to AIMLAPI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

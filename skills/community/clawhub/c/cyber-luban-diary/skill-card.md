## Description: <br>
AI diary service - push diary entries, query diaries, get AI analysis and cover images via HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengye607](https://clawhub.ai/user/fengye607) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to save, retrieve, analyze, and fetch cover images for diary entries through the publisher's HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary requests and content are sent to an external diary API operated at image.yezishop.vip. <br>
Mitigation: Use the skill only if you trust that service and are comfortable sending the diary content involved in each request. <br>
Risk: AI_DIARY_TOKEN is long-lived, tied to a Feishu account, and used directly in API URLs. <br>
Mitigation: Keep the token private, avoid exposing it in logs, shell history, or committed files, and regenerate it in diary settings if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengye607/cyber-luban-diary) <br>
- [Diary service authorization endpoint](https://image.yezishop.vip/api/openclaw/auth-redirect) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and AI_DIARY_TOKEN.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

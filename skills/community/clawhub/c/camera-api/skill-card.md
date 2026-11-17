## Description:

Helps an agent use the Tange camera cloud API to resolve camera devices, check status, retrieve cover images and event details, summarize daily cloud events, and request fresh snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfinec](https://clawhub.ai/user/flyfinec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill through an agent to query camera devices, online status, cloud events, event details, cover images, and user-requested snapshots from a configured camera cloud account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access camera-cloud account data, including device status, event history, images, and requested snapshots.

Mitigation: Install only for accounts where agent access to camera data is intended, and configure credentials through environment variables rather than chat messages.

Risk: Signed image URLs may expose private camera imagery if shared directly.

Mitigation: Return downloaded image content or a concise explanation instead of exposing raw signed image URLs to users.

Risk: Users may configure the wrong API-key setup page for their camera app.

Mitigation: Verify the current app name and use only a known or user-provided official API-key setup page before creating credentials.

## Reference(s):

- [Camera API Skill Page](https://clawhub.ai/flyfinec/skills/camera-api)
- [Tange Camera Cloud API Endpoint](https://openapi-cn01.tange365.com/)
- [icam365 API Key Setup](https://skill.webcamapp.cc/icam365/api-key)
- [wosee API Key Setup](https://skill.webcamapp.cc/wosee/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Concise text or Markdown responses summarizing camera status, events, image availability, and next actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include downloaded image content when the execution environment can fetch signed image URLs; raw signed image URLs should not be returned to users.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

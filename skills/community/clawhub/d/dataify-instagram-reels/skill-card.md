## Description:

Collect Instagram Reel records from a Reel URL, Reel-list URL, or website URL. Do not use for profile data, post comments, or Google Shopping products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for Instagram Reel detail, list/profile, or website/list URLs and retrieve the final collected result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-handling risk around the Dataify API TOKEN.

Mitigation: Configure DATAIFY_API_TOKEN outside conversation history, never print or paste the token in chat, and confirm the token is present without exposing its value.

Risk: External runtime trust risk when using the default wait-and-download behavior.

Mitigation: Review and trust the dataify-task-operations runtime before allowing the skill to monitor and download task results.

Risk: Unintended data submission to Dataify.

Mitigation: Use the skill only for Instagram URLs the user intends to send to Dataify, and confirm scope when collection volume or multiple input groups materially changes cost or exposure.

## Reference(s):

- [Modes and parameters](references/modes-and-parameters.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-instagram-reels)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder?platform=1)
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON task/result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN; submits one Dataify Builder task and waits for the final result by default unless no-wait behavior is requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

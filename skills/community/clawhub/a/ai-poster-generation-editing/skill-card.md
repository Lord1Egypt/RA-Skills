## Description:

This skill helps brand, ecommerce, and marketing teams use AI Hive Nano Banana Pro to create, revise, and adapt commercial poster artwork with production zones for editable copy, legal text, QR codes, and channel-specific layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, and marketing teams use this skill through an agent to plan and submit controlled poster-generation, poster-revision, and channel-adaptation requests. It is aimed at product launches, events, promotions, exhibitions, recruitment, live streams, store openings, social posts, and print-oriented poster workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI Hive API keys.

Mitigation: Use a virtual environment and provide secrets through an environment variable or safer secret input instead of typing real API keys directly in shell commands.

Risk: Selected poster assets may be uploaded to the AI Hive service.

Mitigation: Install and run only if you trust AI Hive, and upload only assets you are authorized to send to that service.

Risk: Generated downloads may be untrusted files.

Mitigation: Treat downloaded outputs as untrusted until they have been verified before reuse or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-poster-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive OpenAPI endpoint used by the script](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON-style configuration inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can submit requests to AI Hive, upload selected local poster assets, poll task status, and download generated PNG files when executed by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

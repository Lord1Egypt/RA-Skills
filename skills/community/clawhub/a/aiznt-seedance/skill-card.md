## Description:

Seedance Video helps agents submit asynchronous Doubao Seedance text-to-video generation tasks with content-array request bodies and fetch task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to create Seedance video generation tasks from text or media-content prompts and poll until the task succeeds, fails, or times out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured Seedance proxy endpoint can receive the TS_TOKEN bearer credential and submitted prompt or media request data.

Mitigation: Review AIZNT_PROXY_URLS before use and configure only trusted HTTPS endpoints for submit and fetch operations.

Risk: Video generation is asynchronous and fetch operations may continue returning processing states for an extended period.

Mitigation: Poll with bounded intervals and a timeout, and stop when the task reports success or failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/aiznt-seedance)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS; configured proxy endpoints receive the bearer token and submitted request content.]

## Skill Version(s):

1.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

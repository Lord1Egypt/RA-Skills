## Description:

Bole Story Creator calls the Bole AI platform to generate short drama stories, storyboards, and video content from a user prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajianrong](https://clawhub.ai/user/jiajianrong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a brief story idea into a generated short-drama story workflow and a returned video link through the Bole AI platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Bole bearer token may be exposed in stderr logs.

Mitigation: Remove token logging before shared use and avoid running the skill where stderr is retained or visible to other users.

Risk: User story prompts are sent to the external Bole AI platform.

Mitigation: Do not submit confidential, regulated, or sensitive story text unless the Bole account and data handling terms are approved for that use.

Risk: The skill uses a fixed project ID in the video workflow.

Mitigation: Confirm that the project ID is appropriate for the intended Bole account before deployment.

Risk: The skill requires a Bole access key for authentication.

Mitigation: Use a narrowly scoped BOLE_ACCESS_KEY and rotate it if logs or runtime environments may have exposed credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiajianrong/skills/bole-story-creator)
- [Publisher profile](https://clawhub.ai/user/jiajianrong)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing either a result string with story project details and a video URL, or an error string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOLE_ACCESS_KEY and may take several minutes while the external video workflow completes.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

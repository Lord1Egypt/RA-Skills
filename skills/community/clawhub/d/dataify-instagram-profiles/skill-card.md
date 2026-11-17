## Description:

Collect Instagram profile data by username or profile URL. Do not use for post comments or Reel content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs that collect Instagram profile data by username or profile URL, then monitor the task and retrieve the final JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script loads monitoring code from a sibling directory outside the reviewed artifact and gives it the Dataify API token.

Mitigation: Install only if the companion dataify-task-operations runtime and the shared package location are trusted, and review that runtime before use.

Risk: The skill sends Instagram usernames or profile URLs to Dataify and requires a Dataify API token.

Mitigation: Confirm the collection target is appropriate for the use case, keep DATAIFY_API_TOKEN in the environment, and do not paste or print the token in chat or logs.

## Reference(s):

- [Modes and parameters](references/modes-and-parameters.md)
- [Dataify Instagram Profiles on ClawHub](https://clawhub.ai/dataify-server/skills/dataify-instagram-profiles)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN, submits a Dataify Builder task, and by default waits for the final collected result.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

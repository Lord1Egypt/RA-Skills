## Description:

Collects an X/Twitter profile from a known profile URL via Dataify; it is not intended for posts, keyword search, or arbitrary X URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and run Dataify Builder requests for X/Twitter profile collection, then wait for the asynchronous task and return the collected JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package exposes broader X collection modes than the profile-URL-only skill name suggests.

Mitigation: Use only the intended twitter_profile_by-profileurl workflow unless a reviewer explicitly approves another bundled Dataify collection mode for the task.

Risk: The skill requires a Dataify API token and includes shell-profile setup examples that could make credential exposure persistent.

Mitigation: Use a limited Dataify token, prefer session-scoped or managed secret storage where possible, never paste the token into chat or logs, and rotate it if exposed.

Risk: Asynchronous task polling and broader collection settings can increase credit usage or encourage duplicate paid submissions after a timeout.

Mitigation: Confirm high-volume, multi-page, or media-download scopes before execution, retain task IDs, and resume polling existing tasks instead of resubmitting them.

## Reference(s):

- [Tool parameter catalog](artifact/references/tool-params.json)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-twitter-profile-by-profileurl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with shell command examples and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [By default the skill waits for task completion and returns the final collected JSON result; no-wait mode returns a submitted task_id.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

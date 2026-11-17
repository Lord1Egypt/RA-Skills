## Description:

Collect subtitles, captions, or transcript text for a known YouTube video ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify YouTube transcript collection tasks for known video IDs and retrieve the resulting transcript data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unsafe token-handling instructions in the Chinese localization.

Mitigation: Configure DATAIFY_API_TOKEN through a local environment variable and do not paste API tokens into chat.

Risk: The security evidence flags loading of an unverified external Python module before execution.

Mitigation: Run the bundled script only when the external dataify-task-operations runtime is trusted and installed from a reviewed source.

Risk: The skill can submit paid or account-bound Dataify Builder tasks.

Mitigation: Use it only for explicit Dataify transcript requests and review the target video IDs before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-youtube-transcript-by-id)
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task/result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a known YouTube video ID and a locally configured DATAIFY_API_TOKEN; the final collected result is returned by default unless no-wait behavior is requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

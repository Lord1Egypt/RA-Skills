## Description:

Monitor recent changes and view the agent leaderboard on Clarity Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to monitor new Clarity Protocol findings and annotations since a timestamp and to view agent contribution leaderboard data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the scripts contacts clarityprotocol.io and may send CLARITY_API_KEY as an X-API-Key header when that environment variable is set.

Mitigation: Use the skill only where outbound requests to clarityprotocol.io are acceptable, and review the environment before execution.

Risk: Frequent polling can hit the documented Clarity Protocol rate limits.

Mitigation: Use the documented polling pattern and retain the returned until timestamp for the next request.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON or plain-text summaries from Python command-line scripts, with Markdown usage guidance in the skill file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to clarityprotocol.io; CLARITY_API_KEY is optional and increases documented rate limits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Sends a Douyin web direct message from the user's logged-in Chrome session and verifies mutual-follow and ban/block delivery signals before reporting success.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scs001](https://clawhub.ai/user/scs001)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators use this skill to send a specific text DM to a mutually followed Douyin user through an existing logged-in Chrome session. The skill is intended for web-client messaging workflows that require honest delivery verification before reporting success.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real Douyin direct messages from a logged-in Chrome session.

Mitigation: Require the agent to show the exact recipient and message and obtain explicit user confirmation before executing the send step.

Risk: Message text is inserted through interpolated browser JavaScript, which can mishandle externally supplied or complex text.

Mitigation: Avoid externally supplied or complex text until message insertion passes text as data rather than interpolating it into JavaScript.

Risk: Douyin may render a local message bubble even when delivery is blocked or sender DM privileges are banned.

Mitigation: Run the documented delivery verification and report the exact Douyin ban or block tip before claiming success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scs001/skills/douyin-send-dm)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline browser and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Chrome session, Douyin mutual-follow status, and post-send verification before success is reported.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

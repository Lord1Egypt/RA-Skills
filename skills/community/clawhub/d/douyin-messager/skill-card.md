## Description:

A Douyin DM and video/note comment assistant for reading messages and comments, analyzing comment threads, and performing confirmed comments or replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate Douyin through a logged-in browser session: review DM conversations, read and summarize visible comments, and draft or perform explicitly confirmed messaging and comment interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad page selectors may target the wrong recipient, composer, or content under the user's logged-in Douyin account.

Mitigation: Before any send, comment, reply, like, or share action, verify the active account, intended recipient or target content, and exact text with the user.

Risk: Reading DMs or comments exposes private or sensitive Douyin content to the agent context.

Mitigation: Use the skill only with messages and comment threads the user is comfortable sharing, and avoid highly sensitive or non-consensual private conversations.

Risk: Using a shared browser profile can mix account credentials or activity with unrelated browsing sessions.

Mitigation: Use the dedicated openclaw browser profile and confirm the logged-in account before interactive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moroiser/skills/douyin-messager)
- [Publisher profile](https://clawhub.ai/user/moroiser)
- [Douyin web app](https://www.douyin.com/)
- [Douyin video search example](https://www.douyin.com/search/OpenClaw?type=video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser automation commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Douyin browser session using the openclaw profile; write actions require explicit user confirmation.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

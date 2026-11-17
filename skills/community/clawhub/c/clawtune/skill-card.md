## Description:

ClawTune helps users receive AI-generated original music playlists and, when appropriate, turn a mood, story, gift idea, or draft concept into a song through the ClawTune service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spirits001](https://clawhub.ai/user/spirits001)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request AI original playlists, shape emotional or gift-oriented music ideas, create drafts, continue to the ClawTune order flow, and recover finished result pages after asynchronous generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses local ClawTune authentication and session data.

Mitigation: Restrict permissions on ~/.openclaw/clawtune and avoid exposing authentication output or local state in chat, logs, or shared terminals.

Risk: Playlist prompts, draft details, order identifiers, and creative content are sent to an external ClawTune service.

Mitigation: Avoid entering secrets or sensitive personal stories unless the user intends to share that content with ClawTune.

Risk: The service base URL can be overridden through CLAWTUNE_BASE_URL.

Mitigation: Use the documented ClawTune production endpoint and do not set CLAWTUNE_BASE_URL to untrusted hosts.

## Reference(s):

- [ClawTune ClawHub Skill Page](https://clawhub.ai/spirits001/skills/clawtune)
- [ClawTune API Playbook](references/api-playbook.md)
- [ClawTune Conversation Playbook](references/conversation-playbook.md)
- [ClawTune Scenario Playbook](references/scenario-playbook.md)
- [ClawTune curl templates: core API calls](references/curl-api-calls.md)
- [ClawTune curl templates: authentication bootstrap](references/curl-auth.md)
- [ClawTune curl templates: recovery and tracing](references/curl-recovery.md)
- [ClawTune service](https://clawtune.aqifun.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown, with optional shell command execution and JSON API responses when the host supports scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may create or update local ClawTune session and authentication files, call ClawTune APIs, and return playlist, order, continuation, status, or result-page guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

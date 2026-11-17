## Description:

Keeps conversation context compact by summarizing recent exchanges, surfacing pending actions, and producing a short briefing for the next agent turn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davienzomq](https://clawhub.ai/user/davienzomq)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep long OpenClaw-style sessions manageable by replacing bulky chat history with a compact Markdown summary, pending-action list, and recent-turn log before the next model call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation text is written to local files and reused in later prompts.

Mitigation: Avoid secrets, regulated data, credentials, and sensitive business details unless redaction, retention limits, and restrictive file permissions are in place.

Risk: The always-on monitor can continuously rewrite summaries from the conversation history.

Mitigation: Prefer manual, user-approved summary generation unless continuous monitoring is explicitly needed and easy to disable.

Risk: Prior conversation text can carry stale, private, or prompt-injection content into later model calls.

Mitigation: Review the generated summary before use and treat it as untrusted conversation-derived context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davienzomq/skills/context-gatekeeper)
- [Artifact README](README.md)
- [Artifact skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary file with matching plain-text console output and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary sentence count, pending-item count, and recent-turn count are configurable through command-line flags.]

## Skill Version(s):

0.1.1 (source: server release metadata, artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

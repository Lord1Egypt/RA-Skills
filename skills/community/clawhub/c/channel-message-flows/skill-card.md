## Description:

Use when running QA Lab channel message flow evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill from an OpenClaw repository root to run QA Lab evidence for Telegram draft and final message delivery sequencing through QA Channel or Crabline Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial coverage, and several local references could not be matched to bundled files.

Mitigation: Review the skill source and confirm its referenced files are trusted before installing or running the QA flow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/channel-message-flows)
- [QA scenario: channel-message-flows.yaml](qa/scenarios/channels/channel-message-flows.yaml)
- [QA Channel inbound transport](extensions/qa-channel/src/inbound.ts)
- [QA Lab transport](extensions/qa-lab/src/qa-transport.ts)
- [Crabline transport](extensions/qa-lab/src/crabline-transport.ts)
- [Telegram draft streaming](extensions/telegram/src/draft-stream.ts)

## Skill Output:

**Output Type(s):** [Shell commands, QA evidence]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs the channel-message-flows QA scenario for Telegram draft and final delivery sequencing.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

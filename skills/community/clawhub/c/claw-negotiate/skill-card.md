## Description:

APOA-constrained SAFE negotiation on OpenClaw. Two OpenClaws negotiate within user-approved bounds, stream offers in Telegram, and finalize with human-approved sshsign signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanfiguera](https://clawhub.ai/user/juanfiguera)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, investors, and OpenClaw operators use this skill to run a two-party SAFE negotiation with private authorization bounds, Telegram-visible offer rounds, and human-approved sshsign signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduler behavior may be installed or used without clear operator control.

Mitigation: Review OpenClaw cron and scan configuration before installing, use an isolated environment, and remove any scheduler entries when the negotiation workflow is no longer needed.

Risk: Authorization token and secret handling may weaken the promised negotiation bounds.

Mitigation: Use dedicated test credentials, restrict filesystem access to per-chat working directories, and do not use production signing keys until the token handling design is reviewed.

Risk: Telegram and sshsign integrations can expose signing links or negotiation state if misconfigured.

Mitigation: Use dedicated Telegram bots and sshsign keys, deliver signing links only through private DMs, and verify `doctor` checks before running a live negotiation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juanfiguera/skills/claw-negotiate)
- [Demo video](https://www.youtube.com/watch?v=T2Y2Tr__g_k)
- [Y Combinator SAFE documents](https://www.ycombinator.com/documents)
- [APOA](https://github.com/agenticpoa)
- [sshsign](https://github.com/agenticpoa/sshsign)
- [Automated negotiation study](https://hai.stanford.edu/news/the-art-of-the-automated-negotiation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and Telegram-formatted status cards with generated SAFE PDF and audit artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, ssh, OpenClaw, Telegram configuration, and sshsign access.]

## Skill Version(s):

0.1.10 (source: server release evidence; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

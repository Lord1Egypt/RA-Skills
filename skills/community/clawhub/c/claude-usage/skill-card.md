## Description:

Calculate Claude Max subscription usage from OpenClaw session data. Shows credits consumed, weekly budget percentage, 5-hour rate limit window, and per-session breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemodigital](https://clawhub.ai/user/lemodigital)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to estimate Claude Max subscription usage from local session transcripts, including weekly budget consumption, 5-hour rate limit status, per-session usage, and per-model breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local session transcripts may expose session identifiers, token counts, and usage patterns in terminal or JSON output.

Mitigation: Limit scanning with --sessions-dir when appropriate and review generated text or JSON before sharing it.

Risk: Installing the tool from an untrusted or floating package source can introduce supply-chain risk.

Mitigation: Install only from a trusted source and prefer a pinned ClawHub or package version.

Risk: The credit calculation is based on a reverse-engineered formula and may differ from the subscription provider's actual accounting.

Mitigation: Treat the report as an estimate and compare important decisions against the usage information shown in Claude settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lemodigital/skills/claude-usage)
- [OpenClaw](https://openclaw.ai)
- [Claude usage settings](https://claude.ai)
- [Claude limits credit reference](https://she-llac.com/claude-limits)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Terminal text report or JSON emitted by a command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw or Moltbot session JSONL files; saved configuration may store reset time, plan, and timezone.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; package.json states 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

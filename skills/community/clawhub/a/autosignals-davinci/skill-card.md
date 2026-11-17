## Description:

Monitors and controls the AutoSignals autonomous research loop.

This skill is for research and development only.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to check, start, stop, and inspect an autonomous loop that experiments with trading signal logic and backtests proposed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start a persistent autonomous research loop that edits code and consumes compute.

Mitigation: Use it only in an isolated, version-controlled AutoSignals checkout after reviewing the local start, status, monitor, and stop behavior.

Risk: The documented stop command kills a process from a PID file, which can be unsafe if the file is stale or incorrect.

Mitigation: Replace the PID-file kill command with a validated stop script that confirms the target process before termination.

Risk: Trading signal optimization is experimental and may overfit backtests or produce unprofitable strategies.

Mitigation: Treat results as research output only and require out-of-sample validation before using any signal outside the research environment.

## Reference(s):

- [AutoSignals README](artifact/README.md)
- [AutoSignals ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/autosignals-davinci)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Natural language guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local project paths and long-running background processes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

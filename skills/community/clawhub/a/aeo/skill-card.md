## Description:

Renamed to agent-readiness. This skill no longer runs audits; it tells the user how to install the agent-readiness skill that replaces it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arberx](https://clawhub.ai/user/arberx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this legacy skill to find the replacement agent-readiness skill and learn how to install it or run an audit from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may expect this legacy skill to run an audit even though it only explains the rename.

Mitigation: Install agent-readiness from ClawHub or run npx @canonry/agent-readiness@8 with the target URL.

## Reference(s):

- [agent-readiness on ClawHub](https://clawhub.ai/arberx/skills/agent-readiness)
- [agent-readiness changelog](https://github.com/Canonry/agent-readiness/blob/main/CHANGELOG.md#800-2026-11-07)
- [agent-readiness project](https://github.com/Canonry/agent-readiness)
- [Canonry homepage](https://canonry.ai)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Migration and installation instructions; does not perform audits.]

## Skill Version(s):

7.6.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

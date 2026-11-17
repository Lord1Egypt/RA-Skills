## Description:

Activity Control UI provides an anime-style local dashboard for OpenClaw that shows agent activity, session status, token usage, and current tasks in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudagebil11-jpg](https://clawhub.ai/user/rudagebil11-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a local web dashboard for monitoring OpenClaw activity, context usage, active tasks, and status updates during an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated local server can expose agent status and activity if reachable from an untrusted network.

Mitigation: Run it only on trusted machines and networks, prefer binding to 127.0.0.1, and add authentication before exposing it beyond the local host.

Risk: Static file serving path containment may allow unintended files to be served.

Mitigation: Restrict served paths to the intended asset directory and verify path containment before deployment.

Risk: The dashboard loads an external Google Fonts stylesheet, which may be unsuitable for privacy-sensitive or offline environments.

Mitigation: Remove the external font request or self-host the font when privacy, network isolation, or offline operation matters.

Risk: The ws dependency is resolved through a non-default npm mirror in the lockfile.

Mitigation: Update the dependency from a trusted registry and verify lockfile integrity before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rudagebil11-jpg/skills/activity-control-ui)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Local web dashboard with JSON status responses, WebSocket activity messages, and CLI broadcast commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays recent activity history, token usage, task state, and session status; requires Node.js and the ws package.]

## Skill Version(s):

1.1.0 (source: server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

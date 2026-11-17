## Description:

Echo patches a locally installed OpenClaw Control UI so completed assistant replies can play selectable Web Audio chimes in the browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use Echo to add, configure, remove, or re-apply an audible browser cue for completed assistant replies in the OpenClaw Control UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release persistently modifies every detected OpenClaw UI installation with injected JavaScript.

Mitigation: Install only after reviewing the payload, run without sudo or administrator privileges, and use remove.sh to restore from backups when the patch is no longer wanted.

Risk: OpenClaw updates or an upstream completion-sound feature can change the patched UI files or make the local patch unnecessary.

Mitigation: Re-run apply.sh after OpenClaw updates only when needed, and prefer the upstream feature when it becomes available.

Risk: The browser cue depends on the current OpenClaw web UI DOM and Web Audio user-gesture behavior.

Mitigation: Use the manual verification checklist after installation and expect the cue to fail quietly if the UI anchor changes or the browser AudioContext is not unlocked.

## Reference(s):

- [Echo ClawHub skill page](https://clawhub.ai/symbolstar/skills/echo-cue)
- [symbolstar ClawHub publisher profile](https://clawhub.ai/user/symbolstar)
- [OpenClaw completion-sound upstream PR #73894](https://github.com/openclaw/openclaw/pull/73894)
- [OpenClaw completion-sound issue #69186](https://github.com/openclaw/openclaw/issues/69186)
- [Manual verification checklist](artifact/tests/manual.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local patch install, removal, re-apply, and browser localStorage configuration steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

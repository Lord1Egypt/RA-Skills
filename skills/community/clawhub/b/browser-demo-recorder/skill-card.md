## Description:

Record browser demo videos from a plain-language brief by turning the requested flow into a plan, driving the OpenClaw browser via CDP, encoding an MP4, writing the output into the workspace `media/` directory, and returning it with the MEDIA protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smile618](https://clawhub.ai/user/smile618)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn a browser walkthrough request into a repeatable recording plan, execute it in an OpenClaw browser, and return a recorded demo video. It is suited for product demos, site walkthroughs, landing-page captures, and hover, click, search, typing, or scroll flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recording plans can execute page-side JavaScript.

Mitigation: Use only plans from trusted sources and review any evaluate steps before running the recorder.

Risk: The skill can control and record browser pages, including pages opened in the configured browser profile.

Mitigation: Run it with a dedicated, non-authenticated browser profile and avoid recording sensitive sessions.

Risk: Typed text may be persisted in debug logs.

Mitigation: Do not put passwords, tokens, or other secrets in recording plans, and review debug JSON before sharing outputs.

Risk: Plans can choose browser endpoints and output paths.

Mitigation: Keep the browser endpoint local and keep outputs inside the workspace media directory.

## Reference(s):

- [Plan Schema](references/plan-schema.md)
- [Example Skills Video Plan](references/example-skills-video-plan.json)
- [ClawHub skill page](https://clawhub.ai/smile618/skills/browser-demo-recorder)
- [Publisher profile](https://clawhub.ai/user/smile618)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Configuration]

**Output Format:** [Short text status with a MEDIA path, plus an MP4 video file and debug JSON written to the configured media directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recording plan may include URLs, viewport settings, timed browser steps, output directory, browser endpoint, and typed text.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

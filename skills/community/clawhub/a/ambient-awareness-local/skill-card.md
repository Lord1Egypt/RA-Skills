## Description:

Provides a lightweight always-on awareness layer that polls local sensors, scores events, and writes significant observations for an OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palxislabs](https://clawhub.ai/user/palxislabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local environmental sensors, monitor configured filesystem paths, and queue attention-worthy events for notification or agent follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The continuous daemon can record local file activity in state files.

Mitigation: Keep watched paths narrow, avoid home and credential directories, and run the prune script on a schedule.

Risk: Notifications may send file-activity summaries outside the local machine.

Mitigation: Use an explicit recipient target, test with dry-run mode, and confirm that the notification channel is appropriate for the watched data.

Risk: Audio, vision, or custom sensors can expand the skill's privacy impact.

Mitigation: Leave audio and vision stubs disabled and review any sensor code and retention settings before enabling it.

Risk: Observed text, speech, OCR, ASR, or file content may contain untrusted instructions.

Mitigation: Treat sensor content as observations only and require explicit confirmation before sensitive external actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/palxislabs/skills/ambient-awareness-local)
- [README](artifact/README.md)
- [Security policy](artifact/policies/security_policy.md)
- [Attention policy](artifact/policies/attention_policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus JSON and JSONL runtime records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime behavior includes deterministic notification messages, local state files, and bounded retention tooling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

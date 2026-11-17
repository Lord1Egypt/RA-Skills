## Description:

FreeRide manages free OpenRouter models for OpenClaw by ranking available models, configuring fallbacks, and updating openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goozdx-eng](https://clawhub.ai/user/goozdx-eng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure OpenClaw with free OpenRouter models and fallback routing when model rate limits occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change OpenClaw's default model and fallback list.

Mitigation: Back up ~/.openclaw/openclaw.json and review the generated model routing before restarting OpenClaw.

Risk: Install instructions and dependency versions are unpinned or inconsistent across the release evidence.

Mitigation: Review the install command, prefer the documented free-ride slug, and pin installer and Python dependency versions where possible.

Risk: Watcher or daemon mode can automatically rotate models after rate-limit checks.

Mitigation: Use watcher or daemon mode only after explicitly opting into automatic model rotation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goozdx-eng/skills/freerid)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenRouter](https://openrouter.ai)
- [Artifact-declared FreeRide repository](https://github.com/Shaivpidadi/FreeRide)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may update OpenClaw model settings, a local model cache, and optional watcher state.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files also list 1.0.0, 1.0.1, and 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

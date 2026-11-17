## Description:

Generate a playful or sharp daily roast of recent Strava activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranasalalali](https://clawhub.ai/user/ranasalalali)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch recent Strava activity, summarize a selected day, and produce a concise roast-style recap with configurable tone and spice. It supports deterministic CLI output and an OpenClaw runtime path that can use a connected model for one final paragraph with deterministic fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Strava activity data and OAuth token files, then may refresh tokens during normal operation.

Mitigation: Use the narrowest Strava scopes that satisfy the workflow, keep token and config files owner-readable only, and run the skill away from unrelated secrets.

Risk: The reauthorization flow can execute a local helper script when the helper path exists.

Mitigation: Inspect or remove the reauth helper before use, and pass only a trusted helper path when reauthorization is required.

Risk: Model-assisted roast generation could introduce invented stats or react to untrusted activity titles.

Mitigation: Use deterministic data preparation, treat activity names as labels only, sanity-check generated paragraphs, and fall back to deterministic roast output when grounding or style checks fail.

## Reference(s):

- [Daily Strava Roast design notes](references/design.md)
- [Daily Strava Roast V2](docs/V2.md)
- [ClawHub skill page](https://clawhub.ai/ranasalalali/skills/daily-strava-roast)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON payloads and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Roasts are intended to be concise, grounded in supplied Strava activity, and limited to one short paragraph when using the model-assisted runtime path.]

## Skill Version(s):

0.2.5 (source: server evidence, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

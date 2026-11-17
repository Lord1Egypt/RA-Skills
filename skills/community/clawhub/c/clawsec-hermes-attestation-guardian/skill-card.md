## Description:

Hermes-only runtime security attestation and drift detection skill for operator-managed Hermes infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate and verify Hermes runtime posture attestations, detect baseline drift, refresh advisory verification state, and apply guarded verification checks before enabling or scheduling Hermes security workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduler setup can modify the current user's crontab when run with `--apply`.

Mitigation: Preview the managed cron block first, review cadence and command arguments, and apply it only from a pinned or signed release path.

Risk: An unsigned advisory-feed bypass can persist if scheduled with `--allow-unsigned`.

Mitigation: Avoid scheduling unsigned bypass mode; if used for emergency recovery, remove it immediately and restore signed advisory verification.

Risk: Incorrect Hermes home, watch path, feed URL, or skill-directory permissions can weaken attestation or advisory checks.

Mitigation: Verify `$HERMES_HOME`, watch paths, feed endpoints, trust anchors, and skill-directory permissions before enabling recurring jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-hermes-attestation-guardian)
- [ClawSec Hermes documentation](https://clawsec.prompt.security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON security artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write attestation JSON, checksum files, advisory cache/state files, and managed user crontab blocks when the operator explicitly applies scheduler setup.]

## Skill Version(s):

0.1.7 (source: server release metadata, skill frontmatter, skill.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

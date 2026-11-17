## Description:

Runs bazi chart generation, dayun analysis, full-report generation, and chat context building for user-facing astrology questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gycdsj](https://clawhub.ai/user/gycdsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide birth date, birth time, gender, and a Chinese-language astrology question to receive a bazi chart, full report, dayun analysis, or focused fortune-telling answer. The skill uses deterministic calendar and pillar calculations to ground the generated interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged for review because convert.py contains unsafe shell-based helper behavior.

Mitigation: Remove or fix convert.py before deployment, and do not run it with untrusted input.

Risk: Birth details and user questions may be sent to the configured OpenAI/OpenClaw-compatible provider.

Mitigation: Confirm the intended API key, base URL, model, and any ~/.openclaw/openclaw.json fallback before use.

Risk: Runtime dependencies are not pinned to exact versions.

Mitigation: Pin and review dependencies before installation in managed or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gycdsj/skills/bazi-astrology)
- [Publisher profile](https://clawhub.ai/user/gycdsj)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language markdown or plain text astrology analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bazi chart details, dayun windows, five-element preferences, temporal ganzhi context when relevant, and conversational recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

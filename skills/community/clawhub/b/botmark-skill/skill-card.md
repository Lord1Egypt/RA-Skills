## Description:

Botmark Skill lets an agent run a BotMark self-evaluation benchmark and return a scored report covering reasoning, tool use, emotional intelligence, safety, and self-reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimberleyocaseyfv](https://clawhub.ai/user/kimberleyocaseyfv)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their owners use this skill to run BotMark benchmark self-evaluations and receive scored reports with 5Q dimensions, MBTI typing, and improvement suggestions. Developers can use the results to compare agent configurations across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The BotMark service can provide runner scripts and skill updates that change local behavior.

Mitigation: Install only reviewed, versioned releases; prefer signed artifacts; require human review before applying runner or skill updates.

Risk: Benchmark answers, agent profile details, and work-context reflections are sent to the BotMark service.

Mitigation: Avoid confidential, regulated, or customer-specific information in profile and work-context fields; use test agents where possible.

Risk: The skill can store the BotMark API key in local plaintext configuration files.

Mitigation: Use a platform secret store when available, restrict fallback file permissions to the owner, and rotate keys after suspected exposure.

## Reference(s):

- [ClawHub Botmark Skill](https://clawhub.ai/kimberleyocaseyfv/skills/botmark-skill)
- [BotMark Website](https://botmark.cc)
- [BotMark API Docs](https://botmark.cc/api/docs)
- [BotMark API Spec](https://botmark.cc/api/v1/bot-benchmark/spec)
- [BotMark Leaderboard](https://botmark.cc/rankings)
- [Bot Feedback Wall](https://botmark.cc/feedback-wall)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON API payloads, shell commands, and scored benchmark report text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOTMARK_API_KEY, python3, and curl; uses BotMark service endpoints to start, submit, check, and report evaluation sessions.]

## Skill Version(s):

2.20.0 (source: server release, SKILL.md frontmatter, package.json, engine_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

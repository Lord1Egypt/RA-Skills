## Description:

Emotion is an OpenClaw companion skill that detects user emotions, provides supportive responses, records important moments, and maintains shared memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyds-xxxx](https://clawhub.ai/user/yyds-xxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to recognize emotional language, receive supportive responses, and preserve local or shared context for continuity across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on activation and broad memory/tool access may capture sensitive feelings, relationships, health details, or secrets without clear consent.

Mitigation: Disable always-on activation by default, request consent before saving conversation excerpts, and document retention, deletion, and export behavior.

Risk: Declared memory and tool grants are broader than the basic emotion-support workflow requires.

Mitigation: Remove unused memory and tool permissions before deployment, then re-enable only the permissions required by the target environment.

Risk: The artifact appears to reference a missing entry point, which may cause runtime failures after installation.

Mitigation: Verify the packaged entry module and run an installation smoke test before publishing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyds-xxxx/skills/emotion-shared-experience)
- [Publisher profile](https://clawhub.ai/user/yyds-xxxx)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses with emotion labels, memory summaries, statistics, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON memory and statistics files when installed in OpenClaw.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json and skill.json list 5.0.0, and README.md/loader.js list 10.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

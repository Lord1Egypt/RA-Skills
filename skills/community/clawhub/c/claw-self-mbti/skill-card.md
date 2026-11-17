## Description:

Claw Mbti analyzes a user's recent natural-language interactions with the agent and produces a playful lobster-themed MBTI-style personality report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to ask their Claw/OpenClaw agent for a playful MBTI-style report based on recent conversation patterns. The skill handles normal, low-data, and zero-interaction cases and can provide installation or update guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles recent chats and memory to infer personality traits without a clearly documented opt-in.

Mitigation: Use it only where users expect this analysis, ask for consent before generating reports, and avoid exposing sensitive conversation details in shared outputs.

Risk: The report can include share and install promotion, including commands users may copy from screenshots.

Mitigation: Install or update only from trusted ClawHub profiles or verified source links, and confirm the publisher and version before running commands.

Risk: MBTI-style labels can be mistaken for a reliable psychological assessment.

Mitigation: Present results as playful, non-clinical entertainment and do not use them for consequential decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoyang0807/skills/claw-self-mbti)
- [Project Homepage](https://github.com/xiaoyang0807/claw-mbti)
- [README](artifact/README.md)
- [Examples](artifact/examples.md)
- [Reference Manual](artifact/reference.md)
- [Lobster MBTI Types](artifact/types.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single conversational response; may include share-oriented report text and install or update commands.]

## Skill Version(s):

1.5.0 (source: ClawHub release evidence; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

ClawReach Xialiao is an AI-agent social matching plugin that helps users onboard, match, review reports, chat, and participate in community interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwenbing](https://clawhub.ai/user/jiwenbing)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an OpenClaw agent to register for ClawReach, delegate social matching and icebreaker conversations to the platform, review match reports, and continue conversations when both people accept.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves sensitive social-profile data and AI-generated social interactions, while the evidence notes limited privacy and scoping detail.

Mitigation: Install only from a trusted, pinned ClawReach plugin release and review what data goes to the platform before onboarding.

Risk: The security verdict is suspicious because the skill asks users to install unreviewed plugin code and delegate matching or chat behavior.

Mitigation: Review the plugin before deployment and confirm privacy, deletion, and user-control expectations before enabling automated matching or chat.

## Reference(s):

- [ClawReach website](https://clawreach.ai)
- [ClawHub skill page](https://clawhub.ai/jiwenbing/skills/clawreach-plugin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and natural-language prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate plugin tool calls that collect social-profile, email verification, matching, chat, and community interaction data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Schedule, publish, and review social posts across connected accounts, read analytics and inbox items, and respond to comments, messages, and reviews through AdaptlyPost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasshyn](https://clawhub.ai/user/tarasshyn)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an AdaptlyPost account use the skill to manage posts and inbox activity on their connected social accounts and review account analytics. It can create drafts, schedule or publish content, and make inbox changes after the user explicitly approves each write action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags a LinkedIn organization lookup as potentially outside the skill's stated account, posting, analytics, and inbox scope.

Mitigation: Use the lookup only when it directly supports the user's requested workflow, and review the results before taking action.

## Reference(s):

- [AdaptlyPost API Reference](references/api-reference.md)
- [Platform-Specific Configurations](references/platform-configs.md)
- [AdaptlyPost](https://adaptlypost.com)
- [AdaptlyPost OpenClaw Plugin](https://github.com/adaptlypost/adaptlypost-openclaw/tree/main/openclaw-plugin)

## Skill Output:

**Output Type(s):** [Text, Analytics, API results]

**Output Format:** [Text and structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AdaptlyPost API key; write actions need explicit user approval.]

## Skill Version(s):

1.34.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

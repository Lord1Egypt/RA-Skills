## Description:

This skill guides an agent to help users break down short-video links into shot plans, generate per-shot images and videos on the aidaoyan66 AI video platform, estimate credit costs, and assemble remixed MP4 videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhigao61](https://clawhub.ai/user/chenzhigao61)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and ecommerce marketers use this skill to transform short-video references into editable storyboards and an AI-assisted remix production workflow. The agent can help rewrite prompts, estimate platform credits, guide model choices, and surface compliance reminders for publishing generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes use of a third-party AI video service that may require an account, user-supplied short-video links, and paid platform credits.

Mitigation: Tell users when actions happen on the external platform, verify current pricing in the platform UI, and present cost estimates as estimates rather than guarantees.

Risk: API keys or publishing tokens could be exposed if copied into files, logs, repositories, or chat output.

Mitigation: Keep platform keys and publishing tokens in environment variables only, and do not print or persist secret values.

Risk: Remixing reference videos can create copyright, platform-policy, or AI-labeling issues when users publish generated content.

Mitigation: Remind users to follow destination-platform AI disclosure rules and avoid directly reusing protected source material without appropriate rights.

## Reference(s):

- [AI Video Platform Guide](references/platform-guide.md)
- [Remix Workflow and Troubleshooting](references/workflow.md)
- [AI Video Platform](https://www.aidaoyan66.online)
- [Remix Tool Entry Point](https://www.aidaoyan66.online/inspiration/remix)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with workflow steps, platform links, cost formulas, and troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform URLs, credit estimates, model-selection advice, compliance reminders, and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

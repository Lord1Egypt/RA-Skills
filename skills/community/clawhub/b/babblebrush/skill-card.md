## Description:

Generate and iteratively edit images. Supports storage, UI for manual editing, history, version branching, time travel, reference images, and multiple AI models and providers with your own API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kivs](https://clawhub.ai/user/kivs)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to create, edit, branch, inspect, and manage BabbleBrush image canvases through the BabbleBrush API. It is useful when an agent needs to guide image workflows, issue API requests, poll asynchronous edits, manage reference images, or configure provider credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BabbleBrush can access images and prompts managed through the service.

Mitigation: Install only when the user is comfortable giving BabbleBrush access to those images and prompts.

Risk: BYOK workflows store provider API keys with BabbleBrush and provider usage can affect billing.

Mitigation: Use dedicated provider keys where possible and monitor provider billing.

Risk: Canvas deletion and other account operations can affect stored image work.

Mitigation: Confirm exact canvas details before delete or destructive operations.

## Reference(s):

- [BabbleBrush website](https://babblebrush.com)
- [BabbleBrush API reference](https://babblebrush.com/api)
- [babbleBrush ClawHub listing](https://clawhub.ai/kivs/skills/babblebrush)
- [OpenClaw skill source](https://babblebrush.com/babblebrush/openclaw/SKILL.md)
- [Claude skill source](https://babblebrush.com/babblebrush/claude/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown]

**Output Format:** [Markdown with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BABBLEBRUSH_API_KEY; API responses may include image URLs, canvas identifiers, version identifiers, status fields, and remaining credits.]

## Skill Version(s):

1.4.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Fliz AI Video Generator helps agents integrate with the Fliz REST API to create, monitor, translate, duplicate, and automate AI-generated videos from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jb-fliz](https://clawhub.ai/user/jb-fliz)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and automation builders use this skill to connect agents and applications to Fliz for text-to-video creation, status polling, translations, duplication, resource listing, and webhook notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runnable examples can create billable Fliz resources or consume API quota.

Mitigation: Review commands before execution, use a dedicated low-privilege Fliz API key, and run creation scripts only when video generation and quota use are intended.

Risk: API keys may be exposed through command-line history or process listings when passed as arguments.

Mitigation: Prefer the FLIZ_API_KEY environment variable and avoid pasting tokens into shared logs, shells, or scripts.

Risk: Submitted text may be processed by the Fliz service and could include sensitive content.

Mitigation: Do not submit confidential, regulated, or unpublished text unless approved for processing by Fliz.

Risk: The webhook example can expose webhook payloads or debug history if deployed publicly without controls.

Mitigation: Use webhook_handler.py as a local demo unless authentication, secured proxying, restricted routes, and limited data retention are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jb-fliz/skills/fliz-ai-video-generator)
- [Fliz website](https://fliz.ai)
- [Fliz API documentation](https://app.fliz.ai/api-docs)
- [Fliz API keys](https://app.fliz.ai/api-keys)
- [API Reference](references/api-reference.md)
- [Enum Values](references/enums-values.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and Python, JavaScript, cURL, and Flask code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated Fliz API calls and scripts that create videos, poll status, list resources, or receive webhook events.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

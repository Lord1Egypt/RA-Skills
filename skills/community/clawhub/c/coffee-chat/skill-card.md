## Description:

Generates a personalized coffee chat playbook by researching a target contact, their company, recent posts, and relevant conversation angles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloriathepenguin](https://clawhub.ai/user/gloriathepenguin)

### License/Terms of Use:


## Use Case:

External users and professionals use this skill to prepare for networking coffee chats with researched company context, profile comparison, specific questions, and talking points. It is especially suited for meeting preparation where public web research and optional X or Notion integrations are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may collect and summarize personal or professional details about a meeting target.

Mitigation: Use only public information for legitimate networking preparation and avoid including sensitive personal details that are unnecessary for the conversation.

Risk: The X scraping workflow and Notion export can send researched personal details to third-party services.

Mitigation: Confirm the user is comfortable with the platform and privacy implications before scraping or exporting, and skip optional integrations when not needed.

Risk: The artifact includes shell examples involving X handles and credential setup.

Mitigation: Do not paste untrusted X handles into shell commands, and store Notion or Apify tokens in a proper credential store instead of a shell profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gloriathepenguin/skills/coffee-chat)
- [Apify account integrations](https://console.apify.com/account/integrations)
- [Notion integrations](https://www.notion.so/my-integrations)
- [Notion append block children API](https://api.notion.com/v1/blocks/${NOTION_PAGE_ID}/children)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown playbook with optional shell commands and Notion API payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a local Markdown playbook and optionally append a playbook summary to Notion when credentials are configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

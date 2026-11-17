## Description:

From topic to published blog post in one conversation, this skill generates SEO- and GEO-optimized articles with AI illustrations and voice-over, creates social media adaptations, sets up automated content sessions, and manages a product knowledge base through Citedy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nttylock](https://clawhub.ai/user/nttylock)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to generate, adapt, schedule, and publish Citedy-powered blog and social content from topics, URLs, or product knowledge. Developers and agents can also use it to register a Citedy agent, call Citedy API workflows, and manage content automation settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content automatically to connected blogs or social accounts.

Mitigation: Set auto_publish=false by default and require a final preview and explicit confirmation before posting or scheduling.

Risk: The skill can delete articles and make persistent account changes such as recurring sessions or webhook registrations.

Mitigation: Require explicit confirmation before deletion, use a named agent during registration, and periodically review active sessions and webhooks.

Risk: The skill relies on a Citedy API key with access to the connected account.

Mitigation: Store CITEDY_API_KEY only in the runtime secret store, limit where it is exposed, and rotate or revoke the key if it is shared accidentally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nttylock/skills/citedy-content-writer)
- [Citedy](https://www.citedy.com/)
- [Citedy Privacy Policy](https://www.citedy.com/privacy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, HTTP, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce article drafts, article URLs, social post previews, schedule details, API request examples, and registration guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

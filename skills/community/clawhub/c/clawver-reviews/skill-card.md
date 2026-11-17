## Description:

Handle Clawver customer reviews. Monitor ratings, craft responses, track sentiment trends. Use when asked about customer feedback, reviews, ratings, or reputation management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:


## Use Case:

Store operators and agents use this skill to list customer reviews, draft or post review responses, monitor sentiment, and configure review webhooks for Clawver stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to post or replace public store review responses.

Mitigation: Require the agent to show the exact response text and obtain approval before publishing or editing a response.

Risk: The skill uses an API key to access review data and create webhooks.

Mitigation: Use a least-privilege API key where available, protect the key from logs and transcripts, and approve webhook destination URLs before creation.

Risk: The webhook verification example may need production hardening.

Mitigation: Review and strengthen signature validation, request parsing, replay protection, and error handling before using the example in production.

## Reference(s):

- [Clawver Reviews skill page](https://clawhub.ai/nwang783/skills/clawver-reviews)
- [Clawver](https://clawver.store)
- [Reviews API Examples](references/api-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAW_API_KEY environment variable and may produce customer-facing review response text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

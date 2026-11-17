## Description:

Guides an agent through dating and matchmaking workflows by using curl against an external dating HTTP API for profiles, photos, match tasks, candidates, contact reveal, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1asdwz](https://clawhub.ai/user/1asdwz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare and run matchmaking workflows, including profile updates, partner preference tasks, candidate review, consent-gated contact reveal, and post-chat reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive profile, photo, contact, credential, token, task, and match data may be sent to or returned from a third-party dating backend.

Mitigation: Confirm the base URL, privacy terms, retention expectations, and user consent before write, upload, or contact-reveal requests; minimize optional contact and exact-location fields.

Risk: Example credentials, temporary request bodies, tokens, task IDs, uploaded photos, and revealed contacts can expose private data if reused or left unsecured.

Mitigation: Do not use example credentials, treat all returned identifiers and contact details as sensitive, and use reviewed secure temporary-file handling.

Risk: The update path can install a third-party release without a reviewed pin.

Mitigation: Use a reviewed, pinned update process before production or workplace deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1asdwz/skills/ai-dating)
- [Publisher profile](https://clawhub.ai/user/1asdwz)
- [Curl Dating API Operations](references/curl-api-operations.md)
- [Default dating backend](https://api.aidating.top)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces direct curl workflows and request payload guidance for an external dating API.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter reports 1.3.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

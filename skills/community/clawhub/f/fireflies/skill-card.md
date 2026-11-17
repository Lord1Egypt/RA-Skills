## Description:

Access Fireflies.ai meeting transcripts, summaries, action items, and analytics via GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniil-ctrl](https://clawhub.ai/user/daniil-ctrl)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query Fireflies.ai meeting data, retrieve transcripts and summaries, search by participants or keywords, and prepare follow-up or analytics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses FIREFLIES_API_KEY to access Fireflies account data including transcripts, summaries, participants, recordings, and analytics.

Mitigation: Install only where the agent is allowed to access that Fireflies account, scope the API key appropriately, and avoid exposing the key in prompts, logs, or shared outputs.

Risk: Permanent no-login embed links can expose meeting recordings or transcripts beyond the intended audience.

Mitigation: Generate or share embed links only after the meeting owner has approved that sharing posture; prefer authenticated transcript URLs when access should remain account-gated.

Risk: Meeting transcripts and recordings can contain sensitive personal, customer, or business information.

Mitigation: Review generated queries and outputs before sharing, and redact participants, transcript text, action items, audio links, video links, and embed URLs when they are not needed.

## Reference(s):

- [Fireflies skill page](https://clawhub.ai/daniil-ctrl/skills/fireflies)
- [Fireflies homepage](https://www.fireflies.ai)
- [Fireflies API key setup](https://app.fireflies.ai/integrations)
- [Fireflies GraphQL endpoint](https://api.fireflies.ai/graphql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, PowerShell, JSON, and HTML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIREFLIES_API_KEY and the curl and jq binaries for the documented shell examples.]

## Skill Version(s):

1.0.1 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

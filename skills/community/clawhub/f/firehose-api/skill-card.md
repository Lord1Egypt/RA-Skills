## Description:

Firehose Web Monitor helps agents manage Firehose taps and rules, validate Lucene queries, and consume matching web pages from the Firehose SSE stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tysg](https://clawhub.ai/user/tysg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to work with the Firehose API: create or manage taps, write and validate Lucene rules, and consume the live SSE match stream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use Firehose API credentials and make network calls to Firehose.

Mitigation: Install only when the agent should work with the user's Firehose account, use scoped tap tokens where possible, and reserve the management key for tap administration.

Risk: Tap or rule delete and update operations can permanently stop matches or revoke tokens.

Mitigation: Review and explicitly approve requested delete or update actions before execution; pause taps instead of deleting them when the goal is temporary suspension.

## Reference(s):

- [Firehose](https://firehose.com)
- [Firehose documentation introduction](https://docs.firehose.com/get-started/introduction.md)
- [Firehose quickstart](https://docs.firehose.com/get-started/quickstart.md)
- [Firehose authentication](https://docs.firehose.com/get-started/authentication.md)
- [Stream overview](https://docs.firehose.com/stream/overview.md)
- [Rules and query syntax](https://docs.firehose.com/stream/rules.md)
- [Streaming SSE](https://docs.firehose.com/stream/streaming.md)
- [Match payload](https://docs.firehose.com/stream/match-payload.md)
- [Tap-token endpoints](https://docs.firehose.com/api-reference/tap-token-endpoints.md)
- [Management-key endpoints](https://docs.firehose.com/api-reference/management-key-endpoints.md)
- [Errors and limits](https://docs.firehose.com/api-reference/errors-and-limits.md)
- [Using Firehose with AI agents](https://docs.firehose.com/resources/ai-agents.md)
- [Firehose full documentation](https://docs.firehose.com/llms-full.txt)
- [ClawHub skill page](https://clawhub.ai/tysg/skills/firehose-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Firehose account credentials supplied through FIREHOSE_MANAGEMENT_KEY and FIREHOSE_TAP_TOKEN.]

## Skill Version(s):

2.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

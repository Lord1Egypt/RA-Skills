## Description:

Helps agents use Apify to run web-scraping actors, manage datasets and storage, and set up scheduled tasks through Maton authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Apify users can ask an agent to run actors, inspect runs and datasets, manage storage, and configure schedules or approved automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maton gateway access to the user's Apify account and exposure of long-lived credentials.

Mitigation: Trust Maton before connecting, prefer OAuth over long-lived API keys, and limit authorization to the needed account and scopes.

Risk: Actor runs consume compute units, and writes can change or delete user resources.

Mitigation: Default to read-only requests and get explicit confirmation before each actor run or write.

Risk: Schedules, webhooks, hosted functions, and trigger destinations may keep operating or forwarding data after the chat ends.

Mitigation: Require approval for each automation and its destination, and remove persistent resources when they are no longer needed.

## Reference(s):

- [ClawHub Apify skill](https://clawhub.ai/byungkyu/skills/apify-api)
- [Maton homepage](https://maton.ai)
- [Apify API reference](https://docs.apify.com/api/v2)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with code blocks and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actor runs can consume Apify compute units; schedules and webhooks may continue after the conversation.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

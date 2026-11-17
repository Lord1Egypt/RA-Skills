## Description:

DataHub for Multi-Domain Data lets agents submit natural-language requests for cross-domain data, poll asynchronous results, add API supplies, and create data bounties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xplore3](https://clawhub.ai/user/xplore3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request e-commerce, finance, social media, recruitment, Web3, sports, news, and other data through DataHub instead of building custom collectors. It can return curated data, raw JSON, or Markdown reports and can help submit new API supplies or bounties when data is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if stored in project configuration files or sent through less controlled channels.

Mitigation: Use DATAHUB_API_KEY from the environment and avoid committing project-level DataHub config files.

Risk: Changing DATAHUB_BASE_URL can redirect queries and API keys to a different endpoint.

Mitigation: Keep DATAHUB_BASE_URL set to https://datahub.codes unless the alternative HTTPS endpoint is intentionally trusted.

Risk: Queries send user-provided data to an external DataHub service.

Mitigation: Do not send confidential or personal data unless the user accepts sharing it with DataHub.

Risk: API-supply and bounty workflows may create account-visible external requests.

Mitigation: Confirm API supply additions and bounty creation with the user before running those actions.

## Reference(s):

- [DataHub API Specification](references/api-spec.md)
- [DataHub Website](https://datahub.codes)
- [DataHub API Documentation](https://datahub.codes/docs)
- [ClawHub Skill Page](https://clawhub.ai/xplore3/skills/datahub)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON responses and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include process IDs, API responses, polling status, curated data summaries, raw API JSON, Markdown reports, and confirmation details for API supply or bounty actions.]

## Skill Version(s):

0.2.4 (source: server release evidence; artifact frontmatter lists 0.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

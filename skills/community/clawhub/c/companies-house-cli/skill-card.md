## Description: <br>
UK Companies House CLI - search companies, profiles, officers, filings, PSC, charges, insolvency, and agent-friendly JSON output aligned with rail-cli and tfl-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan8851](https://clawhub.ai/user/shan8851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query public UK Companies House records through the `ch` CLI. It supports company search, profiles, officers, filings, PSC records, charges, insolvency checks, and stable JSON envelopes for downstream parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party npm CLI and a Companies House API key. <br>
Mitigation: Install only if the npm package publisher is trusted, use a dedicated Companies House API key, and keep the key out of logs and shared shells. <br>
Risk: Lookup queries could include secrets or unrelated sensitive personal information. <br>
Mitigation: Limit queries to the public registry information needed for the task and avoid submitting secrets or unrelated sensitive data. <br>
Risk: Broad person searches and all-page retrieval can fan out requests and consume API quota. <br>
Mitigation: Use pagination controls and `--match-limit` for broad names, and account for the Companies House rate limit. <br>


## Reference(s): <br>
- [companies-house-cli homepage](https://ch-cli.xyz) <br>
- [Companies House developer portal](https://developer.company-information.service.gov.uk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI responses are text or JSON envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `ch` CLI and a Companies House API key; JSON success and error envelopes include ok, schemaVersion, command, requestedAt, and data or error.] <br>

## Skill Version(s): <br>
0.3.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

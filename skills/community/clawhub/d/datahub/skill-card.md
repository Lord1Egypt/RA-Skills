## Description: <br>
DataHub helps agents submit natural-language requests for multi-domain data, poll for results, add API supplies, and create data bounties through the DataHub service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xplore3](https://clawhub.ai/user/xplore3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to request structured data, raw API JSON, or Markdown reports across supported domains without building separate data collection integrations. It is also used to submit new API supply requests or create data bounties when data is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, API keys, and configured request data are sent to DataHub or another explicitly configured base URL. <br>
Mitigation: Use only trusted DataHub endpoints, keep the API key in an environment variable or reviewed config file, and avoid submitting secrets or private account data unless the service terms are acceptable. <br>
Risk: Data bounty workflows may include reward or payment-related details. <br>
Mitigation: Confirm bounty terms with the user before submission and avoid sending payment-sensitive details unless the user understands the DataHub billing and data-use terms. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/xplore3/datahub) <br>
- [Publisher website](https://datahub.codes) <br>
- [DataHub API specification](references/api-spec.md) <br>
- [DataHub API documentation](https://datahub.codes/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may be structured data, raw API JSON, or Markdown reports returned after asynchronous polling.] <br>

## Skill Version(s): <br>
0.2.4 (source: ClawHub release evidence; artifact frontmatter says 0.2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Firehose monitors the web in real time by applying Lucene rules to crawled pages and delivering matching pages over a Server-Sent Events stream. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tysg](https://clawhub.ai/user/tysg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Firehose taps and rules, validate Lucene queries, and stream matching web pages while implementing or discussing Firehose API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create, update, or delete live Firehose taps and rules using API credentials. <br>
Mitigation: Keep credentials scoped, review tap and rule identifiers before changes, and require explicit confirmation before any delete operation. <br>
Risk: Bearer tokens grant access to Firehose resources when used in examples or shell commands. <br>
Mitigation: Use environment variables for credentials, avoid sharing command output that contains tokens, and rotate credentials if exposure is suspected. <br>
Risk: Streaming and rule changes can consume rate limits, quotas, or billable Firehose usage. <br>
Mitigation: Validate queries before saving them, monitor documented rate limits, and review Firehose billing and quota documentation before high-volume use. <br>


## Reference(s): <br>
- [ClawHub Firehose Web Monitor release](https://clawhub.ai/tysg/skills/firehose-api) <br>
- [Firehose homepage](https://firehose.com) <br>
- [Firehose introduction](https://docs.firehose.com/get-started/introduction.md) <br>
- [Firehose quickstart](https://docs.firehose.com/get-started/quickstart.md) <br>
- [Firehose stream overview](https://docs.firehose.com/stream/overview.md) <br>
- [Firehose rules and query syntax](https://docs.firehose.com/stream/rules.md) <br>
- [Firehose streaming SSE documentation](https://docs.firehose.com/stream/streaming.md) <br>
- [Firehose API examples](https://docs.firehose.com/api-reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands, endpoint tables, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus FIREHOSE_MANAGEMENT_KEY and FIREHOSE_TAP_TOKEN environment variables for live API operations.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

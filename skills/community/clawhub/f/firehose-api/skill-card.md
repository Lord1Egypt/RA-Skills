## Description: <br>
Firehose Web Monitor helps agents work with the Firehose API to define Lucene monitoring rules, manage taps, and stream matching web-page events over SSE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tysg](https://clawhub.ai/user/tysg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for Firehose API guidance, curl commands, SSE streaming examples, and Lucene query patterns for monitoring web changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward retrieving broad tap tokens with a management key. <br>
Mitigation: Provide the management key only for explicit administrative tasks and prefer a single intended tap token for streaming and rule work. <br>
Risk: Examples and guidance involve sensitive Firehose bearer tokens. <br>
Mitigation: Avoid displaying full tokens in chat, logs, saved transcripts, or generated command output. <br>
Risk: The documented API includes create, delete, and revoke operations for taps and rules. <br>
Mitigation: Require user confirmation before create, delete, or revoke operations. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/tysg/firehose-api) <br>
- [Firehose homepage](https://firehose.com) <br>
- [Firehose API base URL](https://api.firehose.com) <br>
- [Lucene regular expression syntax](https://lucene.apache.org/core/9_0_0/core/org/apache/lucene/util/automaton/RegExp.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API examples, JSON snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that use curl with FIREHOSE_MANAGEMENT_KEY or FIREHOSE_TAP_TOKEN environment variables.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

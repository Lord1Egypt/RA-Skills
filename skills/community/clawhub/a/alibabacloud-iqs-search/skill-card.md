## Description:

Provides real-time web search and page reading through Aliyun IQS APIs for current information, fact verification, URL content extraction, and web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the web, verify current facts, retrieve news or research sources, and extract readable content from URLs through Alibaba Cloud IQS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and requested URLs are sent to Alibaba Cloud IQS.

Mitigation: Do not submit secrets, private URLs, or proprietary research terms unless they may be shared with Alibaba Cloud.

Risk: The skill requires an Alibaba Cloud IQS API key that may be provided through an environment variable or local config file.

Mitigation: Prefer a session environment variable; if a config file is used, restrict file permissions.

Risk: Deep search mode has materially higher latency and cost than the default engine.

Mitigation: Use the lower-cost Generic or LiteAdvanced engines for normal lookups and reserve Deep mode for complex research needing long page text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-iqs-search)
- [Alibaba Cloud IQS search endpoint](https://cloud-iqs.aliyuncs.com/search/unified)
- [Alibaba Cloud IQS readpage endpoint](https://cloud-iqs.aliyuncs.com/readpage/scrape)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command output from search and page-reading scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include source links and may include snippets, summaries, main text, publication time, hostnames, and relevance scores; page-reading output includes title, URL, content, and status code.]

## Skill Version(s):

0.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

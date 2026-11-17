## Description:

Calls Baidu Qianfan web search APIs with AppBuilder credentials to search the live web and return structured results for Chinese web-heavy, site-filtered, or recency-filtered retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windrunner20](https://clawhub.ai/user/windrunner20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run Baidu Qianfan web searches through a reusable local wrapper, especially for Chinese web retrieval, site-limited search, recent results, and optional image or video result requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can send the user's Qianfan API key to an arbitrary URL when invoked with --url.

Mitigation: Avoid passing keys on the command line, do not let untrusted prompts or automation supply --url, and allowlist the exact Qianfan HTTPS endpoint before routine use.

## Reference(s):

- [Baidu Qianfan Search API Reference](references/api.md)
- [Baidu Qianfan web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [ClawHub skill page](https://clawhub.ai/windrunner20/skills/baidu-smart-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default script output normalizes results into query, count, items, and raw_keys; --raw returns the upstream JSON.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

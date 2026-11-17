## Description:

Browser Search uses a local Chromium browser to run public web searches and extract result titles and links from Bing, Google, Baidu, or DuckDuckGo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshuikeji](https://clawhub.ai/user/linshuikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search public web results without configuring a search API, then collect titles and links for current information lookup, technical documentation discovery, or public market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to public search engines through the local Chromium session.

Mitigation: Do not search for secrets, private identifiers, confidential customer data, or other sensitive terms.

Risk: The skill can write a user-specified output file under the user's home directory.

Mitigation: Review output paths before execution and keep generated result files in an intended project or scratch directory.

Risk: The Playwright dependency is version-ranged rather than pinned.

Mitigation: Pin Playwright in controlled deployments to improve reproducibility.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshuikeji/skills/browser-search)
- [Publisher profile](https://clawhub.ai/user/linshuikeji)

## Skill Output:

**Output Type(s):** [json, text, markdown]

**Output Format:** [JSON response object, with optional saved JSON/TXT/MD search-result file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the query, selected engine, result count, and result entries containing title, URL, and engine.]

## Skill Version(s):

1.0.7 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

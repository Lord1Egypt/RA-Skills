## Description: <br>
安全的网络搜索工具，支持多个搜索引擎。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web or Wikipedia searches, return concise search summaries with titles, snippets, URLs, and source labels, and reuse a local 24-hour cache for repeated queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search providers. <br>
Mitigation: Avoid searching for secrets, credentials, private customer data, or other sensitive text. <br>
Risk: Search history can be retained in the local cache at ~/.ai_search_cache.db. <br>
Mitigation: Clear or disable the cache when local search-history retention is not acceptable. <br>
Risk: Dependency ranges are not pinned to exact versions. <br>
Mitigation: Pin dependency versions in managed environments before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/02) <br>
- [Publisher profile](https://clawhub.ai/user/nidhov01) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Dependency list](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown search summaries with optional Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include titles, snippets, URLs, source labels, and cached results.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

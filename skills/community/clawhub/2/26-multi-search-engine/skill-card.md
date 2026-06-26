## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to form search-engine URLs and web_fetch calls across Chinese and global search engines, including privacy-focused engines and WolframAlpha queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may disclose sensitive information to public search engines. <br>
Mitigation: Do not include passwords, tokens, private URLs, confidential project names, regulated data, or other sensitive information in queries. <br>
Risk: Advanced search operators can broaden or target searches in ways that may return misleading, stale, or sensitive public results. <br>
Mitigation: Keep searches user-directed and review results before relying on or sharing them. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/26-multi-search-engine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with URL templates and inline web_fetch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; queries are sent to public search engines chosen by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

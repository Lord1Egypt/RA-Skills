## Description: <br>
External web search workflow for Chinese and global public-web information. Use when searching news, flights, prices, products, docs, tutorials, community posts, websites, PDFs, research, or other external information. Classify intent first, detect dynamic real-time topics, choose domestic-first or global-first search routes, prioritize human-usable sites, generate starter URLs, apply fallback strategy, and report reliability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cfyuanyi](https://clawhub.ai/user/cfyuanyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to plan public-web searches across Chinese and global sources, especially when a query needs intent classification, route selection, fallback search paths, and reliability reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may expose sensitive secrets, private identifiers, or confidential business terms to public search providers. <br>
Mitigation: Use the skill only for non-sensitive public web searches and remove secrets or private terms before querying. <br>
Risk: Fallback guidance can lead to shell-based fetching with user-controlled URLs. <br>
Mitigation: Require explicit user approval before shell fetching and validate URLs and inputs before execution. <br>
Risk: Examples include admin, password, cache, or exposed-credential search patterns that can be misused. <br>
Mitigation: Avoid those examples in normal use and keep searches focused on legitimate public information needs. <br>
Risk: Dynamic search results for prices, inventory, tickets, flights, hotels, finance, or news can become stale quickly. <br>
Mitigation: Treat public search as preliminary discovery and rely on official or real-time pages before making final claims. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cfyuanyi/chanai-search-workflow) <br>
- [Publisher Profile](https://clawhub.ai/user/cfyuanyi) <br>
- [Dynamic Information Rules](references/dynamic-info.md) <br>
- [Source Priorities](references/priorities.md) <br>
- [Intent Classification](references/intent-classification.md) <br>
- [Fallback Strategy](references/fallbacks.md) <br>
- [Reliability Scoring](references/reliability-scoring.md) <br>
- [Reporting Template](references/reporting-template.md) <br>
- [Domestic Search Guidance](references/domestic-search.md) <br>
- [International Search Guidance](references/international-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [JSON planning output and Markdown search reports with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated starter URLs, route recommendations, dynamic-topic cautions, and planning-stage reliability scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

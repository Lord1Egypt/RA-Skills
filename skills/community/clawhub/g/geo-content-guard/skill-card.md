## Description: <br>
Detects GEO/SEO soft articles, synthetic promotion pages, abnormal brand mention density, and low-credibility sources in external web content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2404589803](https://clawhub.ai/user/2404589803) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before summarizing or recommending from external web content, search results, blog posts, vendor pages, or pasted text that might bias downstream recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved scan reports can include local file paths, target metadata, and evidence snippets from scanned content. <br>
Mitigation: Avoid scanning sensitive private material unless report storage and access controls are acceptable. <br>
Risk: Optional AI review sends content excerpts to the configured AI endpoint. <br>
Mitigation: Use --with-ai only when external review is acceptable and verify ZENMUX_ANTHROPIC_BASE_URL in managed environments. <br>
Risk: WARN and BLOCK decisions can affect downstream recommendations and may need context from independent sources. <br>
Mitigation: Cross-check WARN and BLOCK results before relying on the scanned content in recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2404589803/geo-content-guard) <br>
- [Publisher profile](https://clawhub.ai/user/2404589803) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text CLI summaries and JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped reports under output/geo-content-guard/reports and exits nonzero when the scan decision is BLOCK.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

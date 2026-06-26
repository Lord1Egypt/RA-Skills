## Description: <br>
Searches public web sources for brand-related mentions, removes duplicate URLs, filters results by recency, and returns structured monitoring results for an agent or LLM to review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbniao100](https://clawhub.ai/user/bbniao100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to monitor public brand or product mentions, collect recent negative or reputation-related search results, and hand structured findings to an LLM for downstream risk assessment or summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring results may be noisy or scoped incorrectly if search behavior does not include the brand name in every query. <br>
Mitigation: Review results manually and verify the generated queries cover the intended brand before using outputs for alerts or decisions. <br>
Risk: The skill collects public search results but does not perform final risk classification or alert routing. <br>
Mitigation: Use a downstream reviewer or LLM workflow to classify severity, confirm relevance, and decide whether any alert should be sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bbniao100/brand-sentinel) <br>
- [Configuration example](references/config-example.json) <br>
- [AutoGLM Web Search API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [Plain text or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes brand, run time, time window, keywords, counts, and filtered result items with title, URL, snippet, date status, and parsed date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

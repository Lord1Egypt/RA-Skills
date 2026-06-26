## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, research-ready outputs, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to run authenticated AIsa-backed web, scholar, smart, Tavily, Perplexity Sonar, and multi-source retrieval workflows and turn results into research briefs or comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries, URLs, prompts, and related text to the AIsa service using an API key. <br>
Mitigation: Use the skill only with data appropriate for AIsa, avoid secrets and private internal URLs, and prefer a scoped AISA_API_KEY where possible. <br>
Risk: Different retrieval modes may send data to different AIsa-backed search and research endpoints. <br>
Mitigation: Review `python3 scripts/search_client.py --help` and choose the narrowest mode that fits the task before submitting sensitive or high-value research prompts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/aisa-search) <br>
- [Publisher Profile](https://clawhub.ai/user/baofeng-tech) <br>
- [AIsa API Endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the bundled client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; outputs may include search results, source collections, confidence scoring, summaries, or endpoint error details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

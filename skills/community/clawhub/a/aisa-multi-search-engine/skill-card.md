## Description: <br>
AIsa Multi Search Engine lets agents run web, academic, Tavily, smart, Perplexity, extraction, and multi-source searches through a single AIsa API key with confidence scoring and synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to gather web, academic, and deep-research results, extract URL content, and synthesize findings with citations or confidence signals for research and source-discovery tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, research topics, supplied URLs, and extracted page content are sent to AIsa and its integrated providers. <br>
Mitigation: Avoid secrets, internal-only URLs, regulated data, or confidential research unless policy allows external processing. <br>
Risk: The skill requires an AISA_API_KEY that authorizes external API calls. <br>
Mitigation: Use a scoped API key, keep it in approved configuration or environment storage, and rotate it if exposed. <br>
Risk: Search results, citations, and synthesized answers can be incomplete, stale, or misleading. <br>
Mitigation: Use confidence summaries as triage signals and independently verify important claims against primary sources. <br>


## Reference(s): <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference) <br>
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/aisa-multi-search-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with search results, extracted content, synthesized answers, citations, and confidence summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and may call AIsa-backed external search providers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, target metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

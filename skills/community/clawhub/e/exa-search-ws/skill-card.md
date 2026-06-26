## Description: <br>
Semantic search, web scraping, and content extraction optimized for AI agents and LLMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to perform semantic web search, retrieve clean Markdown from web pages, collect highlights, and find similar links for research or RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, private URLs, or regulated data submitted to Exa may expose sensitive information to an external web-search service. <br>
Mitigation: Use non-sensitive prompts and public URLs only, and avoid confidential, internal, or regulated data unless you have approval to send it to Exa. <br>
Risk: Broad crawling, live crawling, or large result sets can retrieve untrusted external content or access sites outside the intended research scope. <br>
Mitigation: Set narrow result counts, domain filters, freshness limits, and subpage limits; crawl only sites you have permission to access. <br>


## Reference(s): <br>
- [Exa API & SDK Reference Cheat Sheet](references/api_reference.md) <br>
- [Exa Documentation](https://docs.exa.ai) <br>
- [Exa API Base URL](https://api.exa.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/simonpierreboucher02/exa-search-ws) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python examples; the included command-line utility prints JSON search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXA_API_KEY. Results may include URLs, titles, scores, publication metadata, highlights, extracted Markdown text, and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

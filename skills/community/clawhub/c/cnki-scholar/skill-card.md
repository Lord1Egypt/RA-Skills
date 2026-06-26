## Description: <br>
中文学术论文搜索工具。搜索中英文论文，覆盖知网、万方、维普等中文数据库的论文。Use when: 用户说「搜论文」「查文献」「知网」「CNKI」「搜索中文学术论文」「找中文文献」，或需要搜索、下载、引用中英文论文。支持OpenAlex API（免费，2亿+论文）和Crossref API（DOI覆盖）。Also activate when: 用户需要学术搜索、论文元数据提取、引用格式生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaopanguo](https://clawhub.ai/user/shaopanguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Chinese and English scholarly literature, inspect paper metadata, locate open-access PDF links, and generate citations. It is suited for academic discovery workflows that rely on public scholarly APIs rather than direct CNKI institutional access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, private identifiers, or unpublished project details may be sent to public scholarly APIs when following the examples. <br>
Mitigation: Use non-confidential search terms or sanitize queries before making API calls. <br>
Risk: CNKI-specific coverage may be misunderstood because the skill relies on public scholarly APIs and does not directly access CNKI or institutional subscriptions. <br>
Mitigation: Treat search results as public-index coverage and verify CNKI-only availability through authorized institutional channels. <br>
Risk: Generated citations and metadata may be incomplete or inconsistent for some Chinese-language papers. <br>
Mitigation: Review citation output against the source record before using it in formal academic work. <br>


## Reference(s): <br>
- [CNKI Scholar release page](https://clawhub.ai/shaopanguo/cnki-scholar) <br>
- [OpenAlex fields reference](references/openalex-fields.md) <br>
- [Citation formats reference](references/citation-formats.md) <br>
- [OpenAlex Works API](https://api.openalex.org/works?search=QUERY&per_page=N) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scholarly search queries, paper metadata summaries, open-access PDF availability, and APA, BibTeX, GB/T 7714, or RIS citation text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

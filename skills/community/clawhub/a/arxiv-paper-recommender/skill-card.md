## Description: <br>
推荐高质量的 Agent/RAG 论文；支持 Agent 测评、RAG 测评、Agent 架构和 RAG 架构主题，并自动验证 GitHub 代码与生成结构化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeviosLang](https://clawhub.ai/user/DeviosLang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical readers use this skill to find recent Agent/RAG papers with public GitHub code and receive a concise recommendation report for quick triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts arXiv and GitHub over the network to search papers and verify repositories. <br>
Mitigation: Use it only in environments where those outbound public-data requests are acceptable. <br>
Risk: Recommendation history and generated reports are retained locally under ~/papers. <br>
Mitigation: Review or delete ~/papers/history.json and ~/papers/recommendations on shared machines or when local research history should not be retained. <br>
Risk: Paper summaries and engineering suggestions are derived from abstracts and repository metadata, so recommendations can be incomplete or miss paper limitations. <br>
Mitigation: Review the linked paper, PDF, and repository before relying on a recommendation for technical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeviosLang/arxiv-paper-recommender) <br>
- [arXiv API](https://info.arxiv.org/help/api/index.html) <br>
- [GitHub REST API](https://docs.github.com/rest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendation report with concise terminal summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes recommendation reports under ~/papers/recommendations and keeps local recommendation history under ~/papers/history.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

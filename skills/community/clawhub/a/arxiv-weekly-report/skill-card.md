## Description: <br>
根据 arXiv 学科分类和关键词检索最近一周论文，提炼主要创新点，并生成周报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shu-Ang](https://clawhub.ai/user/Shu-Ang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical teams use this skill to track recent arXiv papers by subject category and keywords, summarize selected papers, and produce a structured weekly research report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses arXiv over the network and can download PDFs for full-text analysis. <br>
Mitigation: Use arXiv IDs or trusted arxiv.org links, and avoid invoking the PDF helper with arbitrary or untrusted PDF URLs. <br>
Risk: Generated reports and optional PDF/text cache files may be written under the local skill directory. <br>
Mitigation: Review stored reports and cache files for sensitive research context before sharing or retaining them. <br>
Risk: Paper assessments may be based on titles, abstracts, or limited extracted pages and can miss details from the full paper. <br>
Mitigation: Treat summaries and ratings as research triage, and verify important claims against the original arXiv paper before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shu-Ang/arxiv-weekly-report) <br>
- [Publisher profile](https://clawhub.ai/user/Shu-Ang) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown report with structured paper summaries, trend observations, recommendations, and optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can save Markdown reports locally and may create optional PDF/text cache files when full-text extraction is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

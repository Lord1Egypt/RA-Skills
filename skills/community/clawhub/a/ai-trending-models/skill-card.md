## Description: <br>
Discovers, collects, ranks, and summarizes recent trending open-source AI and LLM projects from public sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leon0401](https://clawhub.ai/user/leon0401) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and product teams use this skill to monitor recent open-source AI project momentum and receive a ranked, source-linked trend report for follow-up evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs live public web research across multiple third-party sources and saves a local JSON report. <br>
Mitigation: Use it only where outbound requests to the listed public sources and local report output are acceptable; constrain sources and output paths for stricter privacy or network requirements. <br>
Risk: Broad activation and source-use guidance can lead an agent to perform wider research than the user intended. <br>
Mitigation: Confirm the requested scope before running the fetcher or manual fallback, and narrow sources, language filters, or look-back windows when needed. <br>
Risk: Trend reports can become stale or overrepresent the public sources and communities queried by the skill. <br>
Mitigation: Date-stamp outputs, disclose stale data when it is older than three days, and review source coverage before relying on rankings. <br>


## Reference(s): <br>
- [Skill source guide](artifact/references/sources.md) <br>
- [Report template](artifact/references/report_template.md) <br>
- [ClawHub skill page](https://clawhub.ai/leon0401/ai-trending-models) <br>
- [GitHub repository search API](https://api.github.com/search/repositories) <br>
- [Hugging Face trending models](https://huggingface.co/models?sort=trending) <br>
- [arXiv recent AI papers](https://arxiv.org/list/cs.AI/recent) <br>
- [Papers With Code trending](https://paperswithcode.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report with source links, supported by a local JSON data file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes collection date, ranked project tables, category grouping, paper highlights, trend analysis, and stale-data notices when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

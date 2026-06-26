## Description: <br>
Searches recent arXiv papers by topic, prepares daily research digests, and downloads papers for deeper analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[champagne315](https://clawhub.ai/user/champagne315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical readers use this skill to monitor new arXiv papers in configured topic areas and generate daily digests or deeper analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts arXiv, downloads PDFs, and stores generated analysis data locally. <br>
Mitigation: Use it only where arXiv network access and local document caching are expected, and periodically clear cached PDFs and temporary analysis files. <br>
Risk: Prompt-editing commands may write or delete local prompt files under the user's arXiv configuration directory. <br>
Mitigation: Use only the intended prompt templates, such as daily_summary and deep_analysis, until prompt names are restricted by the package. <br>
Risk: The security review flags the release as suspicious because persistent prompt editing and local file behavior are under-scoped. <br>
Mitigation: Review the skill before installing, pin dependencies, and keep writes and deletes inside the intended prompt and cache directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/champagne315/follow-arxiv) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Daily summary prompt](prompts/daily_summary.md) <br>
- [Deep analysis prompt](prompts/deep_analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON command responses and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local configuration, prompt templates, cached PDFs, and temporary JSON data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

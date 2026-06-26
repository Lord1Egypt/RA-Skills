## Description: <br>
Generates and publishes a weekly embodied-AI report by searching ArXiv papers and GitHub projects across seven research areas, then producing Markdown and visual HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical teams use this skill to monitor recent embodied-AI papers and open source projects, summarize trends, and prepare a weekly report for publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing workflow can change a live GitHub Pages repository. <br>
Mitigation: Use a dedicated repository or limited deploy key, require git status and git diff review before committing or pushing, and prefer publishing through a branch or pull request. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/jessy-huang/embodied-ai-weekly) <br>
- [ArXiv Search Guide](references/arxiv_search_guide.md) <br>
- [GitHub Search Guide](references/github_search_guide.md) <br>
- [HTML Template Guide](references/html_template_guide.md) <br>
- [ArXiv recent robotics papers](https://arxiv.org/list/cs.RO/recent) <br>
- [ArXiv recent computer vision papers](https://arxiv.org/list/cs.CV/recent) <br>
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and self-contained HTML reports with supporting images and publication commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces weekly ArXiv summaries, GitHub project summaries, visual HTML reports, and GitHub Pages publishing steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

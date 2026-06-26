## Description: <br>
Monitor new papers on arXiv by category, fetch formatted paper summaries, and manage starred papers for later reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[constx1337](https://clawhub.ai/user/constx1337) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research-focused users use this skill to check recent arXiv papers by category, review concise Markdown summaries, and keep a local starred-paper reading list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts arXiv and displays external paper metadata and abstracts. <br>
Mitigation: Use explicit arXiv-related prompts and verify paper details before relying on summaries or links. <br>
Risk: Starred paper metadata is saved locally in the skill artifact's assets/starred.json file. <br>
Mitigation: Review or clear the local starred-paper list when working in shared or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/constx1337/arxiv-watch) <br>
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy) <br>
- [arXiv API query endpoint](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown paper summaries with command output and local JSON starred-paper data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch results include arXiv IDs, authors, categories, submitted dates, abstract previews, and paper links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

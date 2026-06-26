## Description: <br>
Searches and summarizes ArXiv papers for recent research, specific topics, and daily AI paper summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nomorecoding](https://clawhub.ai/user/nomorecoding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use this skill to run structured ArXiv searches for music generation research, deduplicate paper results, and preserve an audit trail of queries and findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow creates local audit files and paper lists under domain-derived output paths. <br>
Mitigation: Review the intended domain and output directory before running the workflow, and avoid path values containing traversal such as ../. <br>
Risk: The bundled search script builds an ArXiv API request from user-provided query text. <br>
Mitigation: Treat the script as a targeted ArXiv helper, review query input before execution, and avoid using it as a hardened general-purpose URL builder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nomorecoding/arxiv-watcher-music) <br>
- [ArXiv API query endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON paper-list output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local research audit files under research/{domain}/search_results when the workflow is executed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

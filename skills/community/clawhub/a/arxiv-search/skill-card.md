## Description: <br>
Retrieve paper metadata from arXiv using keyword queries and save results as JSONL (`papers/papers_raw.jsonl`). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to collect an initial arXiv paper set for literature review, survey, snapshot, and citation workflows. It supports online arXiv API retrieval and offline CSV, JSON, or JSONL import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes broader survey, brainstorming, thesis, and workflow-execution machinery than the narrow arXiv metadata description discloses. <br>
Mitigation: Install it only when that larger research-workflow bundle is intended, review the bundled pipelines before use, and restrict automatic routing. <br>
Risk: Bundled workflow stages may perform broad workspace rewrites or shell-capable actions that are inappropriate for sensitive workspaces. <br>
Mitigation: Run it in a scoped workspace, review proposed commands before execution, and avoid use where broad output rewrites are unacceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/WILLOSCAR/arxiv-search) <br>
- [Domain pack overview](references/domain_pack_overview.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated paper metadata files in JSONL and optional CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 or Python. The metadata script writes `papers/papers_raw.jsonl` and may also write `papers/papers_raw.csv` or append notes to `STATUS.md`.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

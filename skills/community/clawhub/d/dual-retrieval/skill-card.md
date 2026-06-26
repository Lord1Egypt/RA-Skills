## Description: <br>
Combines M-Flow graph topology and QMD BM25 plus vector retrieval to merge and rank results for precise multi-hop and semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sora-mury](https://clawhub.ai/user/sora-mury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to combine M-Flow memory retrieval with QMD local document search, then merge and rank the results for multi-hop and semantic search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access local QMD content and M-Flow configuration. <br>
Mitigation: Review the m-flow-memory dependency, QMD index location, and .env contents before installation or execution. <br>
Risk: Debug, schema, and report-generation behavior may expose retrieved private content from local caches. <br>
Mitigation: Avoid running the debug/schema scripts on sensitive caches and review generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sora-mury/dual-retrieval) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/sora-mury) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code] <br>
**Output Format:** [Markdown reports and Python retrieval result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes merged retrieval results, source labels, scores, metadata, and summary statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

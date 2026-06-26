## Description: <br>
Read and analyze arXiv papers by fetching LaTeX source, listing sections, or extracting abstracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willamhou](https://clawhub.ai/user/willamhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to retrieve public arXiv paper source, inspect section structure, and extract abstracts for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested arXiv IDs are sent to arxiv.org or export.arxiv.org. <br>
Mitigation: Use the skill only for paper IDs appropriate for public arXiv lookup and make users aware that requests contact public arXiv endpoints. <br>
Risk: Returned paper text is remote content and may contain misleading or adversarial instructions. <br>
Mitigation: Treat fetched paper content as untrusted source material and keep agent decisions grounded in the user's request and reviewer judgment. <br>
Risk: A later runtime implementation could diverge from the disclosed read-only host-limited behavior. <br>
Mitigation: Before deployment, verify that the implementation remains read-only and only contacts the documented arXiv hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/willamhou/arxiv-source) <br>
- [arXiv public endpoint](https://arxiv.org) <br>
- [arXiv export endpoint](https://export.arxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, structured data] <br>
**Output Format:** [JSON objects containing paper text, section lists, abstracts, arXiv IDs, and cache status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include flattened LaTeX text; optional controls remove comments, remove appendices, or replace figures with file paths.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

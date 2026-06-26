## Description: <br>
Adaptive Depth Research v6.0 Universal helps agents run configurable, domain-agnostic multi-source research, extract evidence, and produce layered Markdown reports for decision, validation, and audit review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to scan sources such as arXiv, PubMed, PMC, and web sources, structure findings into source cards, and draft executive summaries, validation checklists, and full reports. It is best treated as research assistance that requires human verification before decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain canned, weakly sourced, or misleading claims. <br>
Mitigation: Treat automatic reports as drafts, run sourcing checks, and verify every material claim against the source cards before use. <br>
Risk: Topic names, source URLs, and generated paths may be handled unsafely by the bundled scripts. <br>
Mitigation: Run the skill in a sandbox, use simple non-confidential topic names, and review or disable synthesis scripts before deployment. <br>
Risk: Research topics and source URLs may be sent to external retrieval services. <br>
Mitigation: Avoid confidential inputs and review network and privacy behavior before using the skill in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueylee-dotcom/deep-research-v60) <br>
- [Publisher profile](https://clawhub.ai/user/xueylee-dotcom) <br>
- [SKILL.md](SKILL.md) <br>
- [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) <br>
- [QUALITY_CRITERIA.md](QUALITY_CRITERIA.md) <br>
- [research-config.yaml](config/research-config.yaml) <br>
- [arXiv API](http://export.arxiv.org/api/query) <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov) <br>
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [PMC Open Access file list](https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa_file_list.cgi) <br>
- [OpenAlex API](https://api.openalex.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, source-card Markdown, JSON extraction records, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates research directories with sources, briefs, and reports; automatic outputs require source verification.] <br>

## Skill Version(s): <br>
6.0.1 (source: server release evidence; artifact SKILL.md states 6.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

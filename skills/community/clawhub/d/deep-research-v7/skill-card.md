## Description: <br>
Deep Research v7 helps agents perform domain research, literature reviews, and survey research across sources such as arXiv, PubMed, PMC, Google Scholar, and Semantic Scholar, then produce executive summaries, validation checklists, and full reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, developers, and other external users use this skill to run configurable multi-source research workflows, extract and validate source evidence, and generate layered Markdown reports for decision support and audit review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports an exposed third-party API key and external LLM or relay service use. <br>
Mitigation: Remove and rotate the exposed key before installation, then confirm that each external service is approved for the intended workspace. <br>
Risk: Security evidence reports under-scoped web fetching and authenticated-site behavior. <br>
Mitigation: Run the skill in a sandboxed workspace and avoid cookies or authenticated pages unless authorization and secure credential handling are in place. <br>
Risk: Security evidence reports file-writing behavior that can overwrite report outputs. <br>
Mitigation: Review output paths and run report-generation scripts on copied or version-controlled workspaces before using generated results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueylee-dotcom/deep-research-v7) <br>
- [Research Protocol](artifact/RESEARCH_PROTOCOL.md) <br>
- [Quality Criteria](artifact/QUALITY_CRITERIA.md) <br>
- [Integration Guide](artifact/INTEGRATION.md) <br>
- [arXiv](https://arxiv.org) <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov) <br>
- [OpenAlex API](https://api.openalex.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON/Markdown source cards, and shell or Python command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces layered research outputs, including an executive summary, validation checklist, full report, source cards, and sourcing checks.] <br>

## Skill Version(s): <br>
7.0.0 (source: server release metadata and artifact/clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

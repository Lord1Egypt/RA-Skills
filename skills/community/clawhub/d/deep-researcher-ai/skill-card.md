## Description: <br>
Generates comprehensive academic research papers with citations using a staged workflow for source discovery, synthesis, verification, writing, and quality assurance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roboticresults](https://clawhub.ai/user/roboticresults) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, analysts, and developers use this skill to create long-form academic research papers, literature reviews, source maps, citation lists, and QA reports from a user-provided topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read paper bundles and related project files supplied by the user. <br>
Mitigation: Use it only with files the user is comfortable exposing to the agent, and avoid confidential or unpublished research unless access to external retrieval and APIs is restricted. <br>
Risk: The workflow may use external research, document-generation, or image-generation services. <br>
Mitigation: Review configured services before use and disable external API steps when working with sensitive material. <br>
Risk: Long research papers can contain incorrect claims or weak citations if source retrieval is incomplete. <br>
Mitigation: Apply the included cross-verification, citation integrity, and QA checks before relying on generated papers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/roboticresults/deep-researcher-ai) <br>
- [Research workflow](research_workflow.md) <br>
- [Data sources registry](data_sources.md) <br>
- [Quality assurance checklist](quality_assurance.md) <br>
- [Citation and reference guide](reference_management.md) <br>
- [Research paper template](research_paper_template.md) <br>
- [arXiv API](https://export.arxiv.org/api/query) <br>
- [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/) <br>
- [Semantic Scholar API](https://api.semanticscholar.org/) <br>
- [World Bank Open Data API](https://api.worldbank.org/v2/) <br>
- [IMF Data API](https://api.imf.org/) <br>
- [OECD Statistics](https://stats.oecd.org/) <br>
- [Hugging Face Hub API](https://api.huggingface.co/) <br>
- [GitHub API](https://api.github.com/) <br>
- [Google Patents](https://patents.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown research paper, source notes, citation list, and QA report; optional PDF or DOCX through companion skills.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 30-40 page papers, 15,000-18,000 words, and 40-80 cited sources when sufficient evidence is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Searches academic literature across Semantic Scholar, Crossref, PubMed, and arXiv with filtering, deduplication, sorting, and multiple result formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jibeilindong](https://clawhub.ai/user/jibeilindong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developer agents use this skill to find scholarly papers across public academic databases, refine results by year, citation count, access status, or venue, and export bibliographies or structured result sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and paper metadata are sent to third-party academic database APIs. <br>
Mitigation: Avoid sensitive queries when privacy matters and use personal API keys or a non-sensitive Crossref email. <br>
Risk: Optional result saving can write files to a caller-selected path. <br>
Mitigation: Enable result saving only with an intentional output path and review generated files before reuse. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jibeilindong/academic-literature-search) <br>
- [Semantic Scholar API](https://www.semanticscholar.org/product/api) <br>
- [PubMed API account](https://www.ncbi.nlm.nih.gov/account/) <br>
- [OpenClaw Docs](https://docs.openclaw.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, BibTeX, RIS, HTML, Excel] <br>
**Output Format:** [Markdown by default, with optional structured exports and success/error metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include paper metadata, statistics, formatted result text, and optional saved files at a caller-selected output path.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Find, compare, and obtain datasets or data lakes across ML repositories, cloud public data registries, government portals, scientific archives, geospatial/climate catalogs, NLP corpora, and generic web dataset indexes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosdelfino](https://clawhub.ai/user/carlosdelfino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data scientists, analysts, and agent users use this skill to discover, compare, and plan access to datasets for ML, analytics, RAG, geospatial, climate, NLP, multimodal, BI, and data engineering work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online searches contact public data services and may disclose private query intent. <br>
Mitigation: Use --offline for sensitive searches or when queries should not leave the local environment. <br>
Risk: Download plans can execute local downloads or source CLI commands when --yes is supplied. <br>
Mitigation: Review the dry-run acquisition plan first and only add --yes after checking source, size, license, and access requirements. <br>
Risk: Raw URLs and saved result files can point to untrusted content, especially when local Kaggle or Hugging Face credentials are configured. <br>
Mitigation: Avoid raw --url downloads and untrusted result files; prefer verified catalog results and inspect commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carlosdelfino/dataset-search) <br>
- [Publisher profile](https://clawhub.ai/user/carlosdelfino) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON search results with dataset candidates, access guidance, caveats, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search can run online against public data services or offline with fallback links; downloads are dry-run plans unless explicitly executed with --yes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

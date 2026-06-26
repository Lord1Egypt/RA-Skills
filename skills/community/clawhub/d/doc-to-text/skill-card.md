## Description: <br>
Extracts readable text from .doc and .docx Word documents with MinerU, returning Markdown or JSON text for reading, indexing, and processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert Word documents or document URLs into readable text for data pipelines, search indexing, NLP preprocessing, and document review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-backed MinerU extraction may expose document contents to a third-party service. <br>
Mitigation: Use token-backed extraction only for documents approved for MinerU/OpenDataLab processing, and avoid confidential, regulated, or customer documents unless provider terms and organizational approvals allow it. <br>
Risk: The skill depends on the third-party mineru-open-api CLI and package source. <br>
Mitigation: Install only from trusted package sources, keep MINERU_TOKEN private, and review the CLI/package before use in sensitive environments. <br>


## Reference(s): <br>
- [Doc To Text on ClawHub](https://clawhub.ai/mzlzyca/doc-to-text) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [OpenDataLab MinerU repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; extracted document output is Markdown or JSON depending on MinerU mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api. MINERU_TOKEN is required for .doc files and full extract mode; .docx flash extraction can run without a token.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

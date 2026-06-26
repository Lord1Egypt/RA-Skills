## Description: <br>
Converts Word, PDF, and Excel documents into structured JSON via MinerU extraction and a Markdown-to-JSON parser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kounlong](https://clawhub.ai/user/kounlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base builders use this skill to convert documents such as course materials, standards, reports, and spreadsheets into structured JSON for downstream RAG or data preparation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents may be sent to MinerU during extraction. <br>
Mitigation: Use only documents whose handling is acceptable under MinerU terms, and avoid confidential or regulated documents unless those terms have been approved. <br>
Risk: The MinerU token is passed to the mineru-open-api CLI during conversion. <br>
Mitigation: Use a limited-purpose MinerU token, avoid running on shared systems, and rotate the token if command-line exposure is a concern. <br>
Risk: Generated JSON may be inaccurate or unsuitable for a knowledge base without review. <br>
Mitigation: Review generated JSON before feeding it into retrieval, embedding, or database workflows. <br>


## Reference(s): <br>
- [KB Preparation Patterns](references/kb-prep.md) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, shell commands, guidance] <br>
**Output Format:** [JSON files with optional intermediate Markdown and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api v0.5+ and MINERU_TOKEN for full document extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

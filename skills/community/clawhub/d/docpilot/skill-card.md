## Description: <br>
DocPilot parses documents, extracts schema-based fields with source evidence, and classifies or splits mixed documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankylala](https://clawhub.ai/user/ankylala) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process PDFs, images, Word, Excel, and CSV files for contract review, financial audit, archive organization, form processing, and compliance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user documents to a configurable remote API and may include sensitive credentials in configuration. <br>
Mitigation: Use only documents authorized for the configured endpoint, verify base URL and environment settings before use, replace or remove bundled API key values, and avoid confidential or regulated documents unless the endpoint satisfies data-handling requirements. <br>


## Reference(s): <br>
- [DocPilot ClawHub Skill Page](https://clawhub.ai/ankylala/docpilot) <br>
- [DocPilot Publisher Profile](https://clawhub.ai/user/ankylala) <br>
- [DocPilot API Endpoint](https://docpilot.token-ai.com.cn) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [JSON responses, Markdown text, and generated local JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include document IDs, page counts, extracted fields with evidence, classifications, segments, metadata, and error codes.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

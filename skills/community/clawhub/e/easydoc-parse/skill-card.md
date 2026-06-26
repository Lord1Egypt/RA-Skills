## Description: <br>
Easydoc Parse helps agents use EasyDoc and EasyLink REST APIs to convert unstructured documents into structured JSON or markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sycamore792](https://clawhub.ai/user/sycamore792) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to submit supported document files to EasyDoc or EasyLink parsing APIs, poll for results, and normalize responses for downstream summarization, extraction, or RAG workflows. <br>

### Deployment Geography for Use: <br>
Global, subject to availability and policy requirements for the selected EasyDoc or EasyLink platform. <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents and API keys may be sent to EasyDoc or EasyLink cloud APIs, and the base URL override can redirect them to another host. <br>
Mitigation: Use only organization-approved documents, keep API keys in secure environment variables, and use a base URL override only for explicitly trusted destinations. <br>
Risk: Medical, legal, financial, confidential, or regulated documents may require additional approval before upload to an external parsing service. <br>
Mitigation: Confirm organizational policy permits the upload before using the skill with sensitive or regulated files. <br>


## Reference(s): <br>
- [EasyDoc REST API Reference](references/easydoc-rest-api.md) <br>
- [EasyLink Platform](https://platform.easylink-ai.com) <br>
- [EasyDoc Platform](https://platform.easydoc.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/sycamore792/easydoc-parse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown, text] <br>
**Output Format:** [Markdown guidance with bash commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper can save normalized JSON parse results that include task status, files, markdown, nodes, and raw API responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

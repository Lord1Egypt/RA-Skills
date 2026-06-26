## Description: <br>
Query local and private documents through AnythingLLM RAG, including document search, file or text uploads, document listing, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianmaomao](https://clawhub.ai/user/tianmaomao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill when an agent needs to query or update a local AnythingLLM knowledge base for private documents, PDFs, and uploaded files. It should route unrelated general questions to the default model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports private document handling through an unsafe shell script with a hardcoded API key. <br>
Mitigation: Use only with a trusted AnythingLLM instance, remove and rotate the embedded key, and configure a scoped ANYTHINGLLM_API_KEY before use. <br>
Risk: The security scan flags the upload-text command as unsafe for sensitive documents. <br>
Mitigation: Fix the upload-text command handling and review inputs before using it with sensitive data. <br>
Risk: Document uploads are persistent additions to the AnythingLLM knowledge base. <br>
Mitigation: Confirm the target workspace and treat uploads as retained knowledge-base content rather than temporary chat context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianmaomao/anythingllm-rag) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AnythingLLM query responses may include textResponse and sources for citation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

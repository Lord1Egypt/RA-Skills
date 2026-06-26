## Description: <br>
Builds RAG pipelines with web search and LLM tools for research, fact-checking, grounded responses, and knowledge retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to assemble RAG workflows that retrieve web or URL content, pass it to LLMs, and produce grounded answers, fact checks, summaries, or research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, search results, and extracted document contents may be processed by inference.sh or downstream LLM providers. <br>
Mitigation: Avoid secrets, private business documents, customer data, and regulated information unless approved for those external services. <br>
Risk: Untrusted URLs or large retrieved content can introduce misleading, unsafe, or uncontrolled prompt context. <br>
Mitigation: Require user confirmation before processing untrusted URLs or large retrieved content, and review generated outputs before use. <br>
Risk: Examples interpolate shell variables into JSON inputs, which can break formatting or mishandle unsafe input. <br>
Mitigation: Use a real JSON encoder and quote inputs safely when adapting examples into reusable workflows. <br>


## Reference(s): <br>
- [Ai Rag Pipeline on ClawHub](https://clawhub.ai/okaris/ai-rag-pipeline) <br>
- [inference.sh](https://inference.sh) <br>
- [Adding Tools to Agents](https://inference.sh/docs/agents/adding-tools) <br>
- [Building a Research Agent](https://inference.sh/blog/guides/research-agent) <br>
- [Manual install and checksum verification](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash examples and pipeline patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are instructions and example commands for external search, extraction, and LLM workflows.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Academic Knowledge Base Clawhub helps academic researchers build a local literature knowledge base that combines SmartLib search, user-uploaded research materials, semantic retrieval, citation management, and AI-maintained research topic notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-levee](https://clawhub.ai/user/j-levee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic researchers use this skill to collect SmartLib results, uploaded papers, news, and personal research notes into a persistent local knowledge base, then search, tag, cite, analyze, and export literature or research-session snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores research files, metadata, notes, and vector data under ~/.workbuddy/academic-kb. <br>
Mitigation: Confirm what will be saved before importing private PDFs, unpublished notes, datasets, or bulk search results, and use the skill only where local storage is acceptable. <br>
Risk: SmartLib credentials, email, quota state, literature metadata, or text may be processed by SmartLib or a chosen embedding provider. <br>
Mitigation: Require explicit user confirmation before registration, external searches, uploads, or vectorization, and disclose which provider receives which data. <br>
Risk: The security evidence flags inconsistent guidance around credential reuse and third-party data or API use. <br>
Mitigation: Review the security summary before installation and configure only trusted SmartLib gateway and embedding endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j-levee/academic-knowledge-base) <br>
- [SmartLib](https://www.vipslib.com) <br>
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [SiliconFlow API keys](https://cloud.siliconflow.cn/account/ak) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with tables, JSON knowledge-base records, citation exports, HTML reports, and local file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SmartLib gateway URL, secret, and email; may persist research content under ~/.workbuddy/academic-kb and use external SmartLib or embedding APIs.] <br>

## Skill Version(s): <br>
3.11.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

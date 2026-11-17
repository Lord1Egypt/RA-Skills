## Description:

Academic Knowledge Base helps researchers build and search a local literature knowledge base that combines SmartLib literature retrieval, BM25 keyword search, vector search, citation export, research sessions, and AI-maintained wiki notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and research teams use this skill to search global academic literature, save papers and uploaded research materials into a personal knowledge base, retrieve them with keyword and vector search, manage research sessions, and export citations or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a plaintext gateway secret.

Mitigation: Remove the bundled secret, rotate it before release, and require users to provide credentials through local configuration or a secret store.

Risk: Confidential or unpublished research may be exposed through external SmartLib matching or embedding calls.

Mitigation: Disable external matching and embeddings for sensitive research unless the user has explicitly confirmed the provider, data flow, and consent.

Risk: Privacy and account-handling expectations may be misleading, including registration behavior and email transmission.

Mitigation: Correct the privacy disclosure, require explicit consent before registration, and avoid sending email addresses in URL query strings.

Risk: The skill may persist research data or modify shared cross-skill configuration.

Mitigation: Show the target paths and configuration changes before persistence, and require confirmation for cross-skill config updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j-levee/skills/academic-knowledge-base)
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [SmartLib API](https://www.vipslib.com/)
- [SiliconFlow API keys](https://cloud.siliconflow.cn/account/ak)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, JSON examples, API call patterns, citation exports, and optional HTML report artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local knowledge-base files, research-session snapshots, vector configuration, BibTeX exports, and HTML statistics reports.]

## Skill Version(s):

3.11.3 (source: server release metadata; artifact frontmatter reports 3.11.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

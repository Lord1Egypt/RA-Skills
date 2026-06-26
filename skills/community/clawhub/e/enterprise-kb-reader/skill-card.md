## Description: <br>
Lightweight enterprise knowledge base query system that provides read-only retrieval capabilities for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apanghu](https://clawhub.ai/user/apanghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support agents, and AI agent users use this skill to search existing enterprise knowledge base content for business questions, product information, company policies, procedures, FAQs, and project information. It is intended for read-only retrieval from a knowledge base already initialized and populated by an administrator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read shared internal knowledge base data, including confidential content if the local kb-data directory is accessible. <br>
Mitigation: Install only for users authorized to query the shared enterprise knowledge base and restrict filesystem access to the kb-data directory. <br>
Risk: Query text is sent to DashScope or OpenAI-compatible embedding services, which may expose sensitive prompts or business terms to an external provider. <br>
Mitigation: Use dedicated API keys and deploy only where sending query text to the configured embedding provider is acceptable. <br>
Risk: The documentation describes local-only access, but embedding calls require external API access when configured with DashScope or OpenAI. <br>
Mitigation: Clarify deployment documentation so operators understand which data stays local and which query text is transmitted to embedding services. <br>
Risk: Dependencies are version-ranged rather than pinned, which can introduce supply-chain or reproducibility risk in managed deployments. <br>
Mitigation: Pin dependencies with a lockfile and review updates before deployment in environments with confidential knowledge base content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apanghu/enterprise-kb-reader) <br>
- [Publisher profile](https://clawhub.ai/user/apanghu) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses with command-line examples and retrieval results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only knowledge retrieval results may include document names, similarity scores, content snippets, document lists, or knowledge base statistics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

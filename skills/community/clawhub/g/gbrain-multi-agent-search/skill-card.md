## Description: <br>
Search and manage a local gbrain personal knowledge base with keyword search, semantic search, page lookup, graph traversal, sync, embedding, statistics, and health-check commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[my12121-beep](https://clawhub.ai/user/my12121-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to search, read, link, sync, and maintain content in a local gbrain personal knowledge base. It is suited for personal notes, documents, emails, diary entries, and related knowledge graph exploration when gbrain and a brain repository are already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and embed private local knowledge-base content. <br>
Mitigation: Keep BRAIN_DIR narrow, exclude secrets and highly sensitive files, and review the embedding provider's retention and privacy terms before running sync, query, or embed. <br>
Risk: The skill requires embedding credentials and encourages local command setup. <br>
Mitigation: Provide API keys through runtime environment variables, avoid putting real keys in shared agent instructions, and verify the local gbrain code before running it. <br>


## Reference(s): <br>
- [Gbrain repository](https://github.com/nicepkg/gbrain) <br>
- [ClawHub skill page](https://clawhub.ai/my12121-beep/gbrain-multi-agent-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs command-oriented guidance for local gbrain workflows and depends on the user's local repository, brain directory, and embedding configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

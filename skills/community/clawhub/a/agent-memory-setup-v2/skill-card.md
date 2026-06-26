## Description: <br>
Creates a three-tier memory directory structure for OpenClaw agents and provides configuration guidance for Gemini-based semantic memory search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize local memory files for OpenClaw agents and configure semantic search backed by Gemini embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files can contain sensitive information that may later be sent to Google's Gemini embedding API during memory indexing. <br>
Mitigation: Keep secrets and sensitive data out of memory files and use the Gemini API key only through an environment variable. <br>
Risk: The setup script creates or updates files in the selected workspace. <br>
Mitigation: Run it only in the intended workspace and review the created memory files before enabling indexing. <br>
Risk: The optional Lossless Claw plugin is separate from this setup helper. <br>
Mitigation: Review and install that plugin independently before enabling it. <br>


## Reference(s): <br>
- [Agent Memory Setup v2 on ClawHub](https://clawhub.ai/autosolutionsai-didac/agent-memory-setup-v2) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local memory directories and stub files when the setup script is run by the user.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

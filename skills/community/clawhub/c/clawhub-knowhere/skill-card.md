## Description: <br>
Use the Knowhere OpenClaw plugin to ingest local files or URLs, search stored documents, inspect parsed results, check jobs, and clean up stored document state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ErickThoughts](https://clawhub.ai/user/ErickThoughts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the Knowhere OpenClaw plugin for document ingestion, retrieval, inspection, job handling, and cleanup. It is useful when users need answers grounded in locally ingested files or URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Knowhere plugin and publisher. <br>
Mitigation: Install it only after confirming that the plugin and publisher are trusted for the intended environment. <br>
Risk: Ingested documents or URLs may be stored in the Knowhere scope. <br>
Mitigation: Only ingest content that is acceptable to store in that scope. <br>
Risk: Remove and clear operations may delete stored document state. <br>
Mitigation: Preview or list documents before using cleanup operations. <br>


## Reference(s): <br>
- [Knowhere OpenClaw plugin](https://github.com/Ontos-AI/knowhere-openclaw-plugin) <br>
- [Knowhere ClawHub page](https://clawhub.ai/ErickThoughts/clawhub-knowhere) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON tool payloads, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides tool selection and concise, labeled responses for document workflows.] <br>

## Skill Version(s): <br>
0.1.0-beta.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

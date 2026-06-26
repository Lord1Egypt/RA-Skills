## Description: <br>
Records AI-generated code context and binds checkpoint records to git commits for traceability and audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to preserve audit records for AI-authored code changes, linking prompts, conversation summaries, decisions, metadata, and changed files to the relevant commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint records can capture sensitive prompts, conversation history, reasoning summaries, and metadata in commit-linked files. <br>
Mitigation: Store sanitized summaries by default, exclude secrets and hidden or system instructions, and require confirmation before writing or committing checkpoint files. <br>
Risk: External checkpoint services could expose repository or conversation data if used without approval. <br>
Mitigation: Use external checkpoint services only when they are approved for the repository's data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlang-cn/checkpoints) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with optional JSON checkpoint records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checkpoint records may include prompts, conversation summaries, decision notes, metadata, changed files, and commit hashes when the user approves storing them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

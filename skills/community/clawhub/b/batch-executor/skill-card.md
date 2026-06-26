## Description: <br>
Batch Executor processes large mixed-content corpora by ingesting files, classifying items, triaging by effort and value, delegating work, checkpointing progress, and reporting outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn large file or export dumps into an execution plan, process tasks and ideas in controlled waves, and produce checkpointed reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores raw and derived corpus contents in the workspace, which can expose private exports, secrets, personal data, or sensitive notes. <br>
Mitigation: Use a private workspace, redact sensitive data before processing, and exclude corpus and report paths from git history when needed. <br>
Risk: Large-scale execution and sub-agent delegation can spread sensitive context or act on unintended items from mixed-content dumps. <br>
Mitigation: Review the manifest and execution plan before heavy processing, supervise sub-agent delegation, and pause or block items that need human approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/batch-executor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown manifests, execution plans, progress updates, and final reports; may include code or shell commands depending on corpus items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent corpus, manifest, report, and learning files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

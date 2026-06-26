## Description: <br>
Parallel batch processing of large file sets using sub-agents for summarization, analysis, extraction, and transformation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddpie](https://clawhub.ai/user/ddpie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to divide large file sets into small batches, dispatch parallel sub-agent work, and merge JSON-style results into indexes, summaries, extraction reports, classification outputs, or code analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad directory patterns can include secrets or private records in sub-agent batches. <br>
Mitigation: Scope directories and file patterns deliberately, and exclude secrets or private records unless sharing them is intentional. <br>
Risk: Processed files may contain untrusted instructions that could influence agent behavior. <br>
Mitigation: Treat file contents as untrusted data and instruct sub-agents to ignore embedded operational instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ddpie/batch-file-processor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown, code] <br>
**Output Format:** [Markdown guidance with bash commands and JSON task templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sub-agent batch outputs are expected as JSON arrays that the main agent compiles into final deliverables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

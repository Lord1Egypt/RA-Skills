## Description: <br>
Refactor code safely without changing behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and apply small, behavior-preserving code refactors with validation before and after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refactoring proposals can accidentally change behavior or public interfaces. <br>
Mitigation: Require tests or deterministic characterization checks, keep changes small, rerun validation after meaningful edits, and review proposed code before merging. <br>
Risk: The RedHat-style naming is not verified as official affiliation by the server evidence. <br>
Mitigation: Treat the skill as third-party content from the server-resolved publisher handle and do not assume Red Hat or NVIDIA affiliation. <br>
Risk: Trigger metadata appears malformed in the artifact. <br>
Mitigation: Review invocation behavior before relying on automatic triggers and ask the publisher to correct the metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-refactor-engine) <br>
- [Publisher profile](https://clawhub.ai/user/mzfshark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with summaries, file-change notes, behavior guards, and validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test or build commands supplied by the user for validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Batch Cognition processes bulk prompt batches with alternating PLAY and THINK loops, preserving inputs before item-by-item execution, checkpointing, and value discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to process prompt dumps, file-based prompt lists, and Drive folder contents one item at a time while preserving inputs and recording follow-up value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores full user inputs and can reuse them across future batches. <br>
Mitigation: Use it only for batches that are acceptable to retain locally, and add retention, deletion, and review rules before processing sensitive material. <br>
Risk: Drive folder processing may inspect private or mixed-confidentiality folders with limited upfront consent controls. <br>
Mitigation: Confirm the folder scope before processing and exclude secrets, regulated data, credentials, and confidential folders unless redaction and approval controls are in place. <br>


## Reference(s): <br>
- [Drive Mode](artifact/references/drive-mode.md) <br>
- [Rolling Decay Memory](artifact/references/rolling-decay-memory.md) <br>
- [Batch Cognition on ClawHub](https://clawhub.ai/dodge1218/batch-cognition) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance, Configuration] <br>
**Output Format:** [Markdown with structured batch notes, analysis, action lists, and code or configuration when requested by batch items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local batch records, value stacks, parked items, discarded items, and chain-linked memory summaries when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

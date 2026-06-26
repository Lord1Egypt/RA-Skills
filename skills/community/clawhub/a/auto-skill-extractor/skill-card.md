## Description: <br>
Automatically learns from repeated subagent work and turns qualifying completions into reusable draft skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahajahmed010](https://clawhub.ai/user/wahajahmed010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to detect repeated subagent workflows, create draft skills, and manage promotion or archival after repeated use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback trigger handling may briefly write a transcript summary to local temporary storage. <br>
Mitigation: Use the stdin integration for sensitive work, keep transcript summaries brief and free of secrets, and avoid highly sensitive conversations until the publisher removes or further documents the disk fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wahajahmed010/auto-skill-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/wahajahmed010) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill drafts, JSON action results, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local workspace paths and lifecycle thresholds for draft creation, promotion, and archival.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

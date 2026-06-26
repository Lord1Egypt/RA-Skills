## Description: <br>
Apollo Renal filters noisy conversation context in real time, preserving useful decisions, preferences, active tasks, and open questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to monitor long or noisy conversations, summarize redundant context, and decide when quick filtering or deeper Apollo Dream consolidation is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers may cause context cleanup to run before the user intends it. <br>
Mitigation: Use report-only mode or require explicit confirmation before pruning context. <br>
Risk: Lossy pruning can remove useful conversation state if importance is misclassified. <br>
Mitigation: Keep backups of decisions, preferences, active tasks, and open questions until trigger scope and recovery behavior is verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nic-yuan/apollo-renal) <br>
- [Publisher Profile](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style context cleanup report with shell-script status output and JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only use or explicit confirmation before filtering is recommended because pruning may be lossy.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

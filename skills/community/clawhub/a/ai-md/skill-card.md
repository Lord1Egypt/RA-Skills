## Description: <br>
AI.MD helps agents convert human-written CLAUDE.md or similar LLM instruction files into structured, AI-native Markdown intended to improve instruction compliance and reduce token overhead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sstklen](https://clawhub.ai/user/sstklen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use AI.MD to audit and rewrite persistent assistant instructions into labeled, gate-based Markdown. The skill is aimed at reducing ambiguous prose, token overhead, and missed instruction constraints in agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to inspect and rewrite persistent Claude instruction files, which may contain secrets, private URLs, or sensitive operational details. <br>
Mitigation: Remove secrets and sensitive operational details before use, require a diff before replacement, and review changes before installing or deploying the rewritten instructions. <br>
Risk: The skill calls for multi-model validation, which may send instruction content outside the local environment if the user chooses remote model testing. <br>
Mitigation: Skip multi-model validation or explicitly approve each external model run after checking that the content is safe to share. <br>
Risk: Mutable install commands or unpinned source references can change between review and installation. <br>
Mitigation: Install from a pinned, trusted revision rather than a mutable main-branch command. <br>


## Reference(s): <br>
- [AI.MD ClawHub release](https://clawhub.ai/sstklen/ai-md) <br>
- [Publisher profile](https://clawhub.ai/user/sstklen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured-label examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to persistent assistant instruction files and request review before replacement.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

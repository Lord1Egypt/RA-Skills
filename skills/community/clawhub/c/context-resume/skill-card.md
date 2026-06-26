## Description: <br>
Reconstructs a developer's working context after an interruption by reviewing local project artifacts and summarizing where work left off. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to resume interrupted coding work by reconstructing recent task state, decisions, blockers, and likely next actions from local development artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may review privacy-sensitive local development context, including git state, uncommitted changes, stashes, reflog, TODO comments, test context, timestamps, and recent terminal commands. <br>
Mitigation: Use it only in repositories and shells where that local context is appropriate for agent review, and avoid running it where secrets, credentials, regulated data, or unrelated confidential work may appear. <br>
Risk: Reconstructed context may be incomplete or misleading if local artifacts are stale, partial, or unrelated to the interrupted task. <br>
Mitigation: Treat the briefing as a starting point and verify suggested next actions against the current repository state before making changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcools1977/context-resume) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jcools1977) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with summarized findings and suggested commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill with no external API requirement.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

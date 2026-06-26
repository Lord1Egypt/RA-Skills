## Description: <br>
Never lose context again with a Write-Ahead Log protocol and SESSION-STATE.md working memory that helps an agent preserve context across compaction, restarts, and distractions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leowing](https://clawhub.ai/user/leowing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent working-memory practices to agent instructions. It helps agents write key user details and task state to local Markdown files before context is lost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to automatically persist user details and task context in local memory files, which can capture personal or confidential information without enough scoping. <br>
Mitigation: Require user consent before storing sensitive details, narrow the protocol to specific projects, and define what categories must never be saved. <br>
Risk: Persistent SESSION-STATE.md and daily notes can retain outdated, sensitive, or unwanted information across sessions. <br>
Mitigation: Document how users can review, edit, and delete memory files, and periodically prune stale or unnecessary entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leowing/bulletproof-memory-1-0-0) <br>
- [PARA Second Brain](https://clawdhub.com/halthelobster/para-second-brain) <br>
- [Proactive Agent](https://clawdhub.com/halthelobster/proactive-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown instructions with example SESSION-STATE.md and AGENTS.md snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory protocol guidance; does not call external tools or APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

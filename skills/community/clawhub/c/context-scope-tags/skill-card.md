## Description: <br>
Provides a lightweight chat protocol for explicit context boundaries using [ISO], [SCOPE], [GLOBAL], [NOMEM], and [REM] tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenomenoner](https://clawhub.ai/user/phenomenoner) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to add explicit scope and memory-intent tags to chat messages, reducing topic bleed and clarifying whether prior context or durable memory should apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory intent tags such as [REM] and [NOMEM] are advisory and may not control storage in the host platform. <br>
Mitigation: Use the assistant platform's actual memory and privacy controls for sensitive information. <br>
Risk: Conflicting scope or memory tags can create ambiguous routing intent. <br>
Mitigation: Apply the documented last-tag-wins policy when clear and ask a clarifying question when the user's intent is ambiguous. <br>


## Reference(s): <br>
- [Context Scope Tags on ClawHub](https://clawhub.ai/phenomenoner/context-scope-tags) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown cheat sheet and routing rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory tags are advisory and depend on the host agent's memory support.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

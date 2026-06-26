## Description: <br>
Provide a chronological history of all actions the agent has taken from the beginning (birth) until now. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlueBirdBack](https://clawhub.ai/user/BlueBirdBack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Claw History to ask an agent for an evidence-backed chronological timeline of its available lifetime actions, including source coverage, gaps, and confidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated history can expose sensitive prior session, memory, command-log, or local-path details. <br>
Mitigation: Review available records for secrets, private user content, internal paths, and sensitive operational details before sharing the timeline. <br>
Risk: Incomplete memory files, disabled hooks, or inaccessible sessions can make the lifetime timeline incomplete. <br>
Mitigation: Report missing sources and coverage gaps explicitly, and label entries as confirmed or inferred based on the available evidence. <br>


## Reference(s): <br>
- [Claw History on ClawHub](https://clawhub.ai/BlueBirdBack/claw-history) <br>
- [BlueBirdBack publisher profile](https://clawhub.ai/user/BlueBirdBack) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown timeline with evidence labels, coverage notes, gaps, and confidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source pointers, inferred entries, and explicit limitations when memory files, session history, command logs, or conversation logs are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

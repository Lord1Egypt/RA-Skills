## Description: <br>
Validates owner migration of a ClawHub skill from a personal publisher to an organization publisher with version checks, inspection, and cleanup in a controlled workflow. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub maintainers use this skill to validate that skill ownership can move from a personal publisher to an organization publisher while preserving version history, stats, aliases, and audit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow is intended for maintainer validation and can affect ownership state if run against a real skill. <br>
Mitigation: Use only a controlled throwaway slug, confirm the target publisher before each step, and delete the temporary skill after validation. <br>
Risk: Commands or helper workflows related to moderation, proof publishing, migration, or autoreview may affect live services or share review artifacts. <br>
Mitigation: Review the exact command and target account before execution, and run only when these ClawHub/Convex maintainer workflows are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/codex-owner-move-1778256848) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Procedural validation checklist; no executable script is bundled.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

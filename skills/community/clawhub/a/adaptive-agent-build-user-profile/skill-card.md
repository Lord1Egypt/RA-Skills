## Description: <br>
Builds or updates a user profile memory by observing workspace context, git history, and conversation patterns when first used or when the profile may be outdated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[truenorth-lj](https://clawhub.ai/user/truenorth-lj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to bootstrap and maintain a concise local profile that helps future sessions tailor collaboration style, technical context, and communication preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect broad workspace, git history, memory, and document context that can reveal sensitive personal or work-style details. <br>
Mitigation: Use it only in workspaces where that access is acceptable, and review the generated profile before allowing it to be saved. <br>
Risk: Persisted profile details may be speculative, sensitive, or become stale over time. <br>
Mitigation: Remove speculative or sensitive traits, date current interests, keep the profile concise, and confirm where the profile and index can be edited or deleted. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/truenorth-lj/adaptive-agent-build-user-profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown profile summary and local memory content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profile content is kept under 2KB and includes dated current interests for staleness detection.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

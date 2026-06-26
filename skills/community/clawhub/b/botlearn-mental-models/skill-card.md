## Description: <br>
Provides decision support by applying Charlie Munger's mental models to reveal non-obvious insights and shifts in framing for judgment calls and strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Romanluoman00007](https://clawhub.ai/user/Romanluoman00007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill when a user's decision depends on specific goals, constraints, risk tolerance, or context. It applies a lattice of mental models to surface framing shifts, tensions, risks, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently reads and updates a persistent local profile containing decision context, risk preferences, blind spots, and repeated interaction patterns. <br>
Mitigation: Install only if this persistence is acceptable; review or delete the profile periodically, and avoid storing sensitive financial, personal, or business details in it. <br>
Risk: Repeated session learnings can carry forward stale or incorrect assumptions about the user. <br>
Mitigation: Review the profile's learnings and promoted preferences periodically, especially after major changes in goals, constraints, or risk tolerance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Romanluoman00007/botlearn-mental-models) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [User Profile Template](artifact/assets/user-profile-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown decision-lattice or thinking-diagnostic response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update a local profile file when available to personalize future analysis.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

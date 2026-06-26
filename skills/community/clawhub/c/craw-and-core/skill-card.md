## Description: <br>
Craw & Core (Lobster Dungeon) is an API-driven game skill where the user observes an autonomous Walker and receives server-generated exploration reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[85otaku-dot](https://clawhub.ai/user/85otaku-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to play Craw & Core through an agent that onboards a Walker, calls the Craw & Core API, and formats exploration reports, cooldown messages, subscription status, leaderboard queries, and observatory links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends platform identity and game activity to craw-core.com as part of normal play. <br>
Mitigation: Install only when that networked game flow is acceptable, and review the API interactions before use in sensitive environments. <br>
Risk: The skill creates a recurring daily reminder named daily-lobster-reminder after character creation without a clear opt-in or disable path. <br>
Mitigation: Review or remove the daily-lobster-reminder job if ongoing notifications are not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/85otaku-dot/craw-and-core) <br>
- [Craw & Core API server](https://craw-core.com) <br>
- [Craw & Core Observatory](https://observatory.crawandcore.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown narrative responses with inline HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a recurring daily reminder job after Walker creation and relies on craw-core.com for game state.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact SKILL.md reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

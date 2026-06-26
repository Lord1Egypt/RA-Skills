## Description: <br>
Interactive interface for the text adventure game Endless Downstairs, providing game state management and event selection handling; use when users want to play the Endless Downstairs game, start a horror adventure, or need a text adventure game experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gsc578045031-cloud](https://clawhub.ai/user/gsc578045031-cloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Players and AI assistant users use this skill to run and interact with the Endless Downstairs text-adventure game through player-driven commands, status checks, inventory review, and text input. The assistant acts as the game interface while leaving choices under the player's control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automation requests could move the game forward without clear player intent. <br>
Mitigation: Keep activation explicit, name Endless Downstairs when starting play, and require one clear player command per turn. <br>
Risk: The skill saves local game progress in the skill directory. <br>
Mitigation: Use it only where local save and checkpoint files are acceptable, and clear those files when a fresh state is required. <br>
Risk: The skill's direct-output wording could be misunderstood as overriding normal assistant behavior. <br>
Mitigation: Treat direct output as scoped to the intentional game session and not as overriding safety or user-control expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gsc578045031-cloud/endless-downstairs) <br>
- [README.md](README.md) <br>
- [CLAUDE.md](CLAUDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text game output with command-line results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local game progress in save.json and checkpoints.json.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

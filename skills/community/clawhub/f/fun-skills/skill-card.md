## Description: <br>
Fun Skills helps agents manage game collections and activity ideas, generate jokes, and run quick local entertainment utilities such as guessing games, coin flips, rock-paper-scissors, dice rolls, and fortune prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris7ji](https://clawhub.ai/user/chris7ji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan entertainment, track video and board games, generate jokes for different contexts, and run small local games or randomizers from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The initializer creates the ~/games directory structure and overwrites template files inside it. <br>
Mitigation: Run the initializer only intentionally, review the target paths first, and back up existing ~/games content before execution. <br>
Risk: The release materials claim scheduled retries to install other skills without enough user-control detail. <br>
Mitigation: Do not enable or rely on any scheduled retry or skill-install behavior unless the publisher clearly documents the schedule, target skills, and opt-out controls. <br>


## Reference(s): <br>
- [Fun Skills on ClawHub](https://clawhub.ai/chris7ji/fun-skills) <br>
- [chris7ji publisher profile](https://clawhub.ai/user/chris7ji) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The initializer can create or overwrite files under ~/games when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

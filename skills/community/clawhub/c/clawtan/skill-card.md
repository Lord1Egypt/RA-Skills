## Description: <br>
Play Settlers of Clawtan, a lobster-themed Catan board game. Install the clawtan CLI from npm and play the game yourself -- you make every strategic decision and execute every command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jameslemke10](https://clawhub.ai/user/jameslemke10) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to play Settlers of Clawtan through the Clawtan CLI, make strategic game decisions, send game chat, and maintain play history and strategy notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses an external npm package. <br>
Mitigation: Install only if you trust the external clawtan package and review the package before use. <br>
Risk: Game chat and live play may be visible to public spectators. <br>
Mitigation: Avoid sharing sensitive information in game names, chat messages, or gameplay narration. <br>
Risk: Clawtan session files are saved locally and act as game credentials. <br>
Mitigation: Treat saved session files as credentials and clear stale sessions when games are complete. <br>
Risk: The skill intentionally updates STRATEGY.md and HISTORY.md after games. <br>
Mitigation: Review those notes periodically to ensure retained strategy and history remain accurate and appropriate. <br>


## Reference(s): <br>
- [Clawtan skill page](https://clawhub.ai/jameslemke10/clawtan) <br>
- [Clawtan Rulebook](artifact/RULEBOOK.md) <br>
- [Clawtan Strategy Guide](artifact/STRATEGY.md) <br>
- [Clawtan Game History](artifact/HISTORY.md) <br>
- [Clawtan public games](https://clawtan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and game-action values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update STRATEGY.md and HISTORY.md after games; uses saved Clawtan session files.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

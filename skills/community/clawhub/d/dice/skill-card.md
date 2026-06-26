## Description: <br>
Roll dice, track scores, and manage game stats for tabletop gaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External tabletop players and game facilitators use this skill to log dice-related activity, scores, rankings, challenges, and recent game history from a local command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command text is stored in plaintext local log files and may include private notes if users enter them. <br>
Mitigation: Do not enter secrets or unrelated private information; review and delete ~/.local/share/dice logs or exports when they are no longer needed. <br>
Risk: The artifact behaves more like a local game activity logger than a complete dice roller. <br>
Mitigation: Use it for tracking tabletop activity and verify any dice outcomes or scores before relying on them in play. <br>


## Reference(s): <br>
- [ClawHub Dice skill page](https://clawhub.ai/bytesagain3/dice) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain3) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text command output with optional JSON, CSV, or text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local logs under ~/.local/share/dice and can export accumulated entries.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

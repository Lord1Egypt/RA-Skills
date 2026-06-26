## Description: <br>
Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1215656](https://clawhub.ai/user/1215656) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to list, search, copy, visualize, and analyze local files and directories from a Clawdbot workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests local filesystem read/write capability, and server security evidence reports inconsistent path scoping. <br>
Mitigation: Use only explicit, narrow target directories; avoid elevated privileges; and confirm allowed and denied paths before installation or execution. <br>
Risk: Server security evidence reports that the package is missing the executable it claims to run. <br>
Mitigation: Do not rely on the advertised safety controls until the executable source is present in the package and matches the declared permissions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/1215656/1215656-clawdbot-filesystem-1-0-2) <br>
- [Publisher profile](https://clawhub.ai/user/1215656) <br>
- [Node.js runtime](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return tabular, tree, list, or JSON-formatted filesystem information depending on command options.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json, skill.json, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Starts from a random Flomo note, displays it, recommends related notes, and lets the user continue a multi-step knowledge walk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayshna](https://clawhub.ai/user/jayshna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Flomo notes use this skill to explore connections among their saved notes by starting from a random note and choosing related notes to continue a knowledge walk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Flomo API token is exposed in the public skill instructions. <br>
Mitigation: Remove the embedded token, rotate the exposed credential, and require each user to provide their own Flomo credential through a protected secret or environment variable. <br>
Risk: The skill can expose note contents, note IDs, tags, and walk history to the agent and local storage. <br>
Mitigation: Use the skill only when users accept that visibility, and review local history storage before sharing logs or workspaces. <br>


## Reference(s): <br>
- [Flomo Random Walk release page](https://clawhub.ai/jayshna/flomo-random-walk) <br>
- [Flomo MCP endpoint](https://flomoapp.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown conversation responses with inline shell commands and local JSON history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display full note contents and stores walk history locally when the agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

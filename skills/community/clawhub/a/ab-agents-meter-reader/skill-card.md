## Description: <br>
Read meter readings from photos for electricity day/night tariffs and water meters, save reading history, and generate landlord messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexburrstudio](https://clawhub.ai/user/alexburrstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to extract household utility meter readings from photos, keep a local reading history, and prepare a formatted message for a landlord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected household meter photos and utility-reading context are sent to MiniMax vision tooling. <br>
Mitigation: Use a dedicated low-privilege MiniMax API key and avoid photos that include unrelated private household details. <br>
Risk: Tenant name, apartment address, and utility readings are stored locally in plaintext. <br>
Mitigation: Run the skill only on a trusted user account and restrict access to the local ~/.meter-readings directory. <br>
Risk: The script invokes an unpinned uvx MCP package and silently checks a root OpenClaw credential file. <br>
Mitigation: Review or pin the invoked package before use and provide credentials explicitly from the intended user account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexburrstudio/ab-agents-meter-reader) <br>
- [Project homepage](https://github.com/alexburrstudio/ab-agents-meter-reader) <br>
- [AB Agents Vision (MiniMax)](https://github.com/alexburrstudio/ab-agents-vision) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and landlord messages, with JSON config and reading history files written locally.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local meter image path and MINIMAX_API_KEY; stores configuration and history under ~/.meter-readings.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

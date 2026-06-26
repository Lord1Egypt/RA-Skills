## Description: <br>
Explain bit-cli skill purpose, installation, required setup, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ParinLL](https://clawhub.ai/user/ParinLL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and operate the Bit URL Shortener CLI for creating, listing, inspecting, updating, deleting, and checking click data for short links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Building and installing the upstream CLI from source can introduce supply-chain or local privilege risk. <br>
Mitigation: Review the upstream bit-cli repository before building it and only use sudo for the final install step when the target path requires administrator privileges. <br>
Risk: Bit API keys can be exposed through shared scripts, logs, or command history. <br>
Mitigation: Use the least-privileged BIT_API_KEY available and keep it in environment configuration rather than shared scripts or logs. <br>
Risk: Update or delete commands can change or remove the wrong short link if the ID is incorrect. <br>
Mitigation: Verify link IDs with list or get commands before running update or delete operations. <br>


## Reference(s): <br>
- [Bit CLI source repository](https://github.com/ParinLL/bit-cli) <br>
- [Bit URL Shortener on ClawHub](https://clawhub.ai/ParinLL/bit) <br>
- [ParinLL publisher profile](https://clawhub.ai/user/ParinLL) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bit, git, go, and sudo binaries for the documented install path, and BIT_API_KEY for authenticated Bit API operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

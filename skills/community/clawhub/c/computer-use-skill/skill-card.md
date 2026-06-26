## Description: <br>
Remote Browser automation via CUA (Computer Use Agent). Use when user requires remote browser to do anything. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallcosmos](https://clawhub.ai/user/smallcosmos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to forward explicit browser automation tasks to a remote Computer Use Agent workflow for navigation, search, form interaction, screenshots, scraping, and checkout-style browser actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill forwards broad user tasks to a remote CUA workflow without enough limits or safety guidance for sensitive browser actions. <br>
Mitigation: Use only for explicit browser tasks acceptable to send to the CUA provider, and require separate confirmation before logins, purchases, account changes, uploads, or public posts. <br>
Risk: Referenced execution dependencies are not fully present in the artifact. <br>
Mitigation: Verify the Python wrapper, SDK source, and dependency setup before running any referenced command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallcosmos/computer-use-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are pass-through browser task instructions and streamed execution messages from the CUA workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

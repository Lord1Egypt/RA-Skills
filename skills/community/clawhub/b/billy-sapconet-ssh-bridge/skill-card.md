## Description: <br>
Standard SAPCONET SSH command templates for bird reads, Puppeteer runs, and inbox messaging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run standardized SSH-based SAPCONET checks, bird read placeholders, Puppeteer prerequisite checks, and inbox messaging command templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs commands through SSH against a SAPCONET target, so an incorrect target or overly privileged SSH account can affect the wrong remote environment. <br>
Mitigation: Verify SAPCONET_TARGET before execution and use a least-privileged SSH account for the intended host. <br>
Risk: The message script can allow crafted message text to become commands on the remote SAPCONET host. <br>
Mitigation: Pass message text through stdin or strict quoting before allowing untrusted or variable message content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Highlander89/billy-sapconet-ssh-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SAPCONET_TARGET and SSH access to the intended SAPCONET host.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

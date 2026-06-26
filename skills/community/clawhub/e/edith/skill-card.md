## Description: <br>
Set up Edith smart glasses as an OpenClaw channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samdickson22](https://clawhub.ai/user/samdickson22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to install and configure the Edith smart glasses channel, add a glasses link code, and restart the gateway so they can interact with their OpenClaw agent hands-free. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting cleanup can remove Edith-related OpenClaw configuration without backup or confirmation. <br>
Mitigation: Back up ~/.openclaw/openclaw.json and review the Edith-related channel and plugin entries before allowing cleanup commands to run. <br>
Risk: The setup installs and trusts a separate OpenClaw plugin for the Edith glasses channel. <br>
Mitigation: Install only when the user intends to connect Edith glasses and trusts the openclaw-edith-glasses plugin. <br>


## Reference(s): <br>
- [Edith ClawHub skill page](https://clawhub.ai/samdickson22/edith) <br>
- [Edith service endpoint](https://edith-production-a63c.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request an Edith glasses link code before producing setup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

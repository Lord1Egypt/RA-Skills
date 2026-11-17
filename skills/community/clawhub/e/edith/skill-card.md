## Description:

Edith sets up Edith smart glasses as an OpenClaw channel for hands-free access to an OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdickson22](https://clawhub.ai/user/samdickson22)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect Edith smart glasses to OpenClaw by installing the Edith glasses channel plugin, adding a link code, and restarting the OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs an OpenClaw plugin and restarts the gateway.

Mitigation: Review the plugin source and package identity before installation, and run the gateway restart only when the user expects service interruption.

Risk: The skill stores a glasses link code in OpenClaw configuration.

Mitigation: Validate the link code format with the user and avoid exposing it in logs, transcripts, or shared files.

Risk: Troubleshooting instructions can directly edit OpenClaw configuration and delete entries matching Edith-related names.

Mitigation: Back up openclaw.json first and remove only exact entries created for the Edith glasses channel.

## Reference(s):

- [ClawHub Edith skill page](https://clawhub.ai/samdickson22/skills/edith)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request an Edith link code and propose OpenClaw plugin, channel, gateway, and configuration changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

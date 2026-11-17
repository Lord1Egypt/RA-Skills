## Description:

ais-skill helps agents collaborate with a TorchV AIS knowledge base by routing KB commands for reading, searching, writing, updating, publishing, file transfer, and link generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuchuan01](https://clawhub.ai/user/liuchuan01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to inspect, search, update, publish, and transfer content in a TorchV AIS knowledge base through explicit KB commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles raw KB authentication tokens.

Mitigation: Use a scoped, short-lived token, keep it outside command-line arguments where possible, and avoid copying broad browser session tokens.

Risk: KB commands are sent to a remote AIS execution endpoint.

Mitigation: Install only if the TorchV AIS endpoint is trusted and keep KB_EXECUTE_URL fixed to the intended HTTPS service.

Risk: Upload, download, and overwrite operations can move data between the local environment and AIS.

Mitigation: Review file paths and document codes before transfer, avoid --overwrite unless required, and save downloads to controlled locations.

Risk: Write, move, delete, and publish operations can change persistent knowledge-base content.

Mitigation: Read the target content first, use the smallest necessary operation, and reserve delete, move, and publish actions for explicit user requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuchuan01/skills/ais-skill)
- [KB read operations manual](references/read.md)
- [KB write and structure operations](references/write.md)
- [KB patch update guide](references/update.md)
- [File transfer guide](references/file-transfer.md)
- [TorchV AIS service endpoint](https://bot.torchv.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON or file outputs from KB operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local downloaded files or temporary download links when file-transfer operations are requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

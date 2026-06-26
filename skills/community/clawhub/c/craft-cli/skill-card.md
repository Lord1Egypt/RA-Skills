## Description: <br>
Manage Craft documents through the craft CLI, including listing, searching, creating, updating, deleting, and exporting documents in JSON, table, or Markdown formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerveband](https://clawhub.ai/user/nerveband) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to inspect, search, create, update, delete, and export Craft documents through CLI commands and helper shortcuts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes hardcoded personal and business Craft API URLs. <br>
Mitigation: Replace the API URLs with an intended scoped Craft endpoint and check the active Craft space before running commands. <br>
Risk: The documented CLI can update or delete Craft documents. <br>
Mitigation: Require explicit approval before update or delete operations and verify target document IDs before execution. <br>
Risk: Installation documentation downloads a binary and moves it with sudo. <br>
Mitigation: Verify the binary source and integrity before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerveband/craft-cli) <br>
- [Publisher profile](https://clawhub.ai/user/nerveband) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI responses may be JSON, table, or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the configured Craft API URL and can produce document content or status output from CLI operations.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

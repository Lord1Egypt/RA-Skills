## Description: <br>
Basecamp CLI helps agents and developers manage Basecamp projects, to-dos, messages, people, and campfires through a TypeScript command-line interface using the bc3 API and 37signals Launchpad OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emredoganer](https://clawhub.ai/user/emredoganer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agent workflows use this skill to configure and run authenticated Basecamp CLI commands for listing, creating, updating, completing, and archiving project-management resources. It is suited for Basecamp automation where the operator can review commands that affect projects, to-dos, messages, campfires, and people data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI uses OAuth permissions to read and write Basecamp data, including posting messages, creating tasks, completing tasks, and archiving projects. <br>
Mitigation: Use a dedicated Basecamp integration where possible and require explicit operator approval before running write or archive commands. <br>
Risk: Installing and running the package requires trust in the third-party npm publisher. <br>
Mitigation: Install only when the publisher is trusted and verify the release source, version, and package contents before deployment. <br>
Risk: OAuth client secrets can be exposed through unsafe shell practices. <br>
Mitigation: Keep BASECAMP_CLIENT_SECRET out of shell history and prefer secure environment or secret-management workflows. <br>


## Reference(s): <br>
- [Basecamp bc3 API documentation](https://github.com/basecamp/bc3-api) <br>
- [37signals Launchpad integrations](https://launchpad.37signals.com/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may perform authenticated Basecamp read and write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

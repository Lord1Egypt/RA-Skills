## Description:

Helps agents authenticate to AppFlowy Cloud/GoTrue and call workspace, document, database, search, and collaboration APIs for self-hosted AppFlowy environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balonegit](https://clawhub.ai/user/balonegit)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to build, debug, and operate AppFlowy API workflows, including token retrieval, workspace discovery, page and database updates, search, and collaboration-data repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live AppFlowy workspace, document, database, and collaboration data.

Mitigation: Use a test workspace first, review every workspace, view, and database ID before running write or cleanup commands, and inspect planned payloads before execution.

Risk: The skill handles AppFlowy passwords and access tokens.

Mitigation: Prefer token or environment-based handling over command-line passwords when possible, redact token output from logs and transcripts, and avoid storing credentials in shared files.

Risk: Example configuration and commands may use plain HTTP endpoints.

Mitigation: Prefer HTTPS endpoints for real deployments and confirm base URL and GoTrue URL values before authenticating.

## Reference(s):

- [AppFlowy API Reference](references/appflowy_api_reference.md)
- [Configuration Example](references/config.example.json)
- [Example Commands](examples/README.md)
- [ClawHub Skill Page](https://clawhub.ai/balonegit/skills/appflowy-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown with inline shell commands, Python command examples, and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call live AppFlowy APIs and modify workspace, document, or database content.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

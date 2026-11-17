## Description:

Provides TeamTalk 5 SDK and server/client development guidance, including API usage, SDK detection, setup, source builds, and TeamTalk server configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romeohorvath](https://clawhub.ai/user/romeohorvath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with BearWare TeamTalk 5 clients, servers, language bindings, SDK setup, build workflows, and API integration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup and build workflow can fetch mutable remote TeamTalk source code.

Mitigation: Pin or verify the source revision before building, and inspect the cloned repository before executing build steps.

Risk: The build workflow can run repository-defined Makefile targets with sudo on the host.

Mitigation: Avoid sudo execution on sensitive machines; prefer an isolated container or virtual machine for builds.

Risk: Generated setup or build commands may affect local developer environments.

Mitigation: Review proposed commands before running them and limit execution to systems intended for TeamTalk SDK work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romeohorvath/skills/bearware-teamtalk)
- [TeamTalk 5 SDK API Reference](references/api_reference.md)
- [TeamTalk 5 SDK ChangeLog](references/changelog.md)
- [TeamTalk 5 Download and Build Links](references/download_links.md)
- [TeamTalk 5 upstream repository](https://github.com/BearWare/TeamTalk5)
- [TeamTalk 5 C-API documentation](https://bearware.dk/teamtalksdk/v5.22a/docs/C-API/)
- [TeamTalk 5 .NET documentation](https://bearware.dk/teamtalksdk/v5.22a/docs/NET/)
- [TeamTalk 5 Java documentation](https://bearware.dk/teamtalksdk/v5.22a/docs/Java/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local setup or build commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

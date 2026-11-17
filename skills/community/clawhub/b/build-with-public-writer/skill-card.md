## Description:

Creates technical writing project files for codewithriver through the bwp command, including articles, courses, theory notes, personas, version management, and share links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverfor](https://clawhub.ai/user/riverfor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to initialize a local content workspace and create Markdown templates for articles, course outlines, theory notes, and writing personas. It also provides commands for listing content, committing changes, checking status, and generating local share links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated sharing server can expose local files over the network with weak default credentials.

Mitigation: Use it only in a trusted local project, change the generated credentials immediately, avoid exposing the server outside localhost, and do not serve sensitive directories until path containment is fixed.

Risk: Basic Auth over plain HTTP does not protect credentials on untrusted networks.

Mitigation: Use local-only access or add HTTPS and stronger access controls before sharing beyond localhost.

Risk: Project initialization writes configuration and server code into the target project, and the commit command stages all changes.

Mitigation: Review generated files and git diff before running the server or committing content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/riverfor/skills/build-with-public-writer)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, shell command output, and generated local configuration/code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates files under BWP_PROJECT_ROOT or /home/node/cwr by default; link sharing depends on the generated local server.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

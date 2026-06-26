## Description: <br>
firmenbuchat helps agents use the firmenbuchat CLI to access the Austrian Firmenbuch through HVD WebServices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasogott](https://clawhub.ai/user/pasogott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to configure the firmenbuchat CLI, search Austrian company and document records, download documents, query changes, and troubleshoot API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed if passed directly on the command line or committed in local environment files. <br>
Mitigation: Store the key with the CLI config or a protected environment file, and do not commit secret files. <br>
Risk: The CLI is installed from third-party Homebrew or uv sources. <br>
Mitigation: Install only after reviewing and trusting the publisher and the referenced installation source. <br>
Risk: Large change-document queries may fail for broad date ranges. <br>
Mitigation: Use smaller time windows for change queries when the service returns errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pasogott/firmenbuchat) <br>
- [Project homepage](https://github.com/pasogott/firmenbuch-aip) <br>
- [UV installation source](https://github.com/pasogott/firmenbuch-aip.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for setup, key configuration, company search, document search, downloads, change queries, diagnostics, and global CLI options.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

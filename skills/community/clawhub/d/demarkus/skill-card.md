## Description: <br>
Persistent agent memory and versioned markdown documents over the Mark Protocol (mark://). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ontehfritz](https://clawhub.ai/user/ontehfritz) <br>

### License/Terms of Use: <br>
AGPL-3.0-only <br>


## Use Case: <br>
Developers and agent users use this skill to install or connect to Demarkus, then fetch, publish, append, list, and version markdown documents that persist across agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default local setup installs a long-running network-facing service. <br>
Mitigation: Prefer client-only or remote mode unless a local server is required, and know how to stop or uninstall the daemon before installation. <br>
Risk: The local server can expose UDP 6309. <br>
Mitigation: Restrict UDP 6309 to trusted interfaces and networks. <br>
Risk: Persistent agent memory can retain sensitive personal or project data across sessions. <br>
Mitigation: Avoid storing secrets or sensitive data in Demarkus documents. <br>
Risk: The installer is fetched from a remote script URL. <br>
Mitigation: Inspect and pin the installer before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ontehfritz/demarkus) <br>
- [Publisher profile](https://clawhub.ai/user/ontehfritz) <br>
- [Demarkus homepage](https://demarkus.io) <br>
- [Demarkus installer](https://raw.githubusercontent.com/latebit-io/demarkus/main/install.sh) <br>
- [mcporter call syntax](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/call-syntax.md) <br>
- [mcporter CLI reference](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides setup for local or remote Demarkus servers and emits commands for mcporter-based MCP registration and Mark document operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

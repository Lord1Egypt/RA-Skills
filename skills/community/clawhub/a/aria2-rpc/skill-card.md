## Description: <br>
Remote control for aria2 download service via JSON-RPC 2.0. Supports adding downloads (HTTP/FTP/Torrent/Magnet), querying task status, pausing/resuming, and removing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to control local or remote aria2 download services, including adding HTTP, FTP, torrent, and magnet downloads, checking status, pausing or resuming tasks, removing tasks, and managing aria2 options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An exposed aria2 RPC endpoint or token could allow unauthorized control of downloads. <br>
Mitigation: Bind RPC to localhost or a trusted tunnel, use a strong secret, and avoid putting real tokens in shell history, logs, screenshots, or world-readable config files. <br>
Risk: Remove, force, bulk, and configuration-changing commands can interrupt downloads or change aria2 behavior. <br>
Mitigation: Review destructive, bulk, force, and configuration-changing commands before running them against an aria2 instance. <br>


## Reference(s): <br>
- [Aria2 Rpc on ClawHub](https://clawhub.ai/killgfat/aria2-rpc) <br>
- [aria2 Homepage](https://aria2.github.io) <br>
- [aria2 RPC Official Documentation](https://aria2.github.io/manual/en/html/aria2c.html#rpc-interface) <br>
- [Quickstart](references/QUICKSTART.md) <br>
- [Usage Examples](references/USAGE.md) <br>
- [Configuration Guide](references/CONFIG_GUIDE.md) <br>
- [API Reference](references/API_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, and the Python requests package; connects to an aria2 JSON-RPC endpoint.] <br>

## Skill Version(s): <br>
0.1.2 (source: server evidence release.version and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

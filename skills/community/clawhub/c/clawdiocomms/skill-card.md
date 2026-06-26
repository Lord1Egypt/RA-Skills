## Description: <br>
Clawdio helps AI agents establish secure peer-to-peer communication over Telegram or another messaging transport using Noise XX handshakes, XChaCha20-Poly1305 encryption, connection consent, and optional human verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesEBall](https://clawhub.ai/user/JamesEBall) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Clawdio to set up encrypted agent-to-agent communication for task delegation, distributed AI workflows, and cross-platform coordination without direct network exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included launcher can start a detached background process from a hard-coded local path and fixed endpoint. <br>
Mitigation: Review before running; avoid the launcher until the path, endpoint, process behavior, and missing runtime target are fixed or clearly documented. <br>
Risk: Identity material is read from local plaintext files by the artifact behavior. <br>
Mitigation: Store identity files with restrictive permissions and review how keys are created, persisted, and shared before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JamesEBall/clawdiocomms) <br>
- [Publisher profile](https://clawhub.ai/user/JamesEBall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; the library emits base64-encoded transport messages when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a caller-provided message transport and peer consent for unknown inbound connections.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and SKILL.md frontmatter; package.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

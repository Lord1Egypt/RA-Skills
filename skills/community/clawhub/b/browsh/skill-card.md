## Description: <br>
A modern text-based browser that renders web pages in the terminal using headless Firefox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and terminal-first users use this skill to run Browsh, open specific URLs, and configure the required Browsh and Firefox binaries for terminal web browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Browsh or Firefox binaries could affect terminal browsing sessions. <br>
Mitigation: Install Browsh and Firefox from trusted sources and confirm PATH entries point to trusted binaries before use. <br>
Risk: Browsh is a TUI application and may fail in non-PTY execution environments. <br>
Mitigation: Run Browsh in a PTY-enabled session such as tmux or an agent process configured with PTY support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gumadeiras/browsh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local browsh and firefox binaries; Browsh should run in a PTY session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

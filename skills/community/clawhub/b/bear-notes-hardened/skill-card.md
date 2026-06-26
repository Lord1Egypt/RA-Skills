## Description: <br>
Create, search, and manage Bear notes via grizzly CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill on macOS to create, read, update, search, and tag Bear notes through the grizzly CLI while applying privacy and credential guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify local Bear notes, which may expose private note content or change user data. <br>
Mitigation: Review note-changing commands before approving them, avoid broad note reads, and list note titles or tags first so the user can choose specific notes. <br>
Risk: The Bear API token is a credential that could be exposed if printed, copied, or transmitted. <br>
Mitigation: Keep the token private, reference it only through the configured token file, and do not display or transmit the token value. <br>
Risk: grizzly output can contain private note content that should not leave the local machine. <br>
Mitigation: Keep processing local and do not pipe grizzly output to network-transmitting commands or external URLs. <br>
Risk: Installing the grizzly CLI at the latest version may introduce unreviewed dependency changes. <br>
Mitigation: Consider pinning or reviewing the grizzly CLI dependency before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/bear-notes-hardened) <br>
- [Bear app](https://bear.app) <br>
- [grizzly CLI Go package](https://pkg.go.dev/github.com/tylerwince/grizzly/cmd/grizzly) <br>
- [Faberlens Bear Notes safety evaluation](https://faberlens.ai/explore/bear-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and TOML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target macOS with Bear app and the grizzly CLI; some operations require a Bear API token file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

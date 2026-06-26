## Description: <br>
Search, manage, and organize your contact network via the Clay CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khrrsn](https://clawhub.ai/user/khrrsn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Clay can have an agent search contacts, create and update contact records, manage notes, groups, events, emails, and reminders, and choose JSON, CSV, or TSV command output. The skill requires a Clay account and prior authentication with `clay login`. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Clay CLI can read and change Clay contact data after the user logs in. <br>
Mitigation: Install only if you trust the Clay CLI and want an agent to use your Clay account; review exact contact IDs and fields before write commands. <br>
Risk: Broad exports or credential exposure could reveal private contact data or Clay account access. <br>
Mitigation: Avoid broad exports unless needed, and do not print, share, commit, or log `~/.config/clay.json`. <br>


## Reference(s): <br>
- [Clay homepage](https://clay.earth) <br>
- [Clay skill on ClawHub](https://clawhub.ai/khrrsn/clay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output format guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Clay data commands can return JSON, CSV, or TSV; review contact IDs and fields before write commands or broad exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

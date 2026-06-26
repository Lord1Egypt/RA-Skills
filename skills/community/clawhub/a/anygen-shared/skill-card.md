## Description: <br>
anygen CLI: Shared patterns for authentication, global flags, and output formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supertilico2001](https://clawhub.ai/user/supertilico2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as a shared reference for authenticating to the anygen CLI, applying standard flags, discovering commands, and formatting safe user-facing responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references Anygen credentials, including ANYGEN_API_KEY and API-key login flows. <br>
Mitigation: Do not print or expose API keys or auth tokens; prefer scoped Anygen credentials when available. <br>
Risk: The Anygen CLI may read or upload local files, create tasks, or change account state. <br>
Mitigation: Ask for explicit user confirmation before commands that read files, upload files, create tasks, or modify the Anygen account. <br>
Risk: Use depends on the external @anygen/cli package. <br>
Mitigation: Install and run the package only when the publisher and package source are trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the anygen CLI and either an ANYGEN_API_KEY value or an authenticated login session.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

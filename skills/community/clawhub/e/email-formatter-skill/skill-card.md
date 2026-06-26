## Description: <br>
Transform rough email drafts into polished, professional messages by improving grammar, tone, clarity, and email formatting while preserving the sender's intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and agents use this skill to polish email drafts, convert notes into complete messages, adjust tone for business recipients, and check grammar, readability, and security-sensitive content before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can automatically install optional Python packages and alter the local Python environment. <br>
Mitigation: Review setup behavior before installation, prefer an isolated environment or virtual environment, and do not allow automatic pip installs with --break-system-packages. <br>
Risk: The skill creates persistent helper files under the user's home directory. <br>
Mitigation: Inspect the installed files and permissions before use, and remove the skill workspace when it is no longer needed. <br>
Risk: Email drafts may contain sensitive personal, financial, health, credential, or business information. <br>
Mitigation: Avoid processing highly sensitive drafts unless local command-line handling and temporary or persistent files are acceptable for the user's privacy and compliance requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cerbug45/email-formatter-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional command-line analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rewritten email text, tone and readability findings, grammar suggestions, security warnings, or refusal guidance for blocked content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

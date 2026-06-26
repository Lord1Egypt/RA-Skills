## Description: <br>
Protect AI agents from email-based attacks including prompt injection, sender spoofing, malicious attachments, and social engineering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivaavimusic](https://clawhub.ai/user/ivaavimusic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add email-security checks before an agent reads email content, acts on email-based commands, or handles attachments. It supports sender verification, content sanitization, threat detection, and provider-specific guidance for Gmail, AgentMail, Proton Mail, and generic IMAP/SMTP systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Owner or admin emails may trigger broad agent actions without enough confirmation controls. <br>
Mitigation: Configure owner, admin, and trusted sender lists before use, require confirmation for command execution and destructive actions, and avoid relying on SPF or DKIM alone for privileged commands. <br>
Risk: Attachments saved from email remain untrusted files even after parsing. <br>
Mitigation: Apply strict attachment type policies, scan saved files before use, and treat all saved attachments as untrusted until independently reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivaavimusic/email-security) <br>
- [Owner Configuration](artifact/references/owner-config.md) <br>
- [Security Policies](artifact/references/security-policies.md) <br>
- [Threat Patterns](artifact/references/threat-patterns.md) <br>
- [Gmail Provider Guide](artifact/references/provider-gmail.md) <br>
- [AgentMail Provider Guide](artifact/references/provider-agentmail.md) <br>
- [Generic Email Provider Guide](artifact/references/provider-generic.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and JSON-capable script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts for parsing email, sanitizing content, and verifying senders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

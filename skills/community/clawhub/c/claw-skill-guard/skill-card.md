## Description: <br>
Security scanner for OpenClaw skills. Detects malicious patterns, suspicious URLs, and install traps before you install a skill. Use before installing ANY skill from ClawHub or external sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentchan](https://clawhub.ai/user/vincentchan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to scan OpenClaw skills before installation, review suspicious commands or URLs, and add optional workflow controls such as an AGENTS.md policy or pre-commit hook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner findings can miss sophisticated obfuscation or produce false positives. <br>
Mitigation: Treat results as advisory and manually review flagged lines before installing or approving a skill. <br>
Risk: Remote ClawHub scans fetch and unpack skill archives from untrusted sources. <br>
Mitigation: Scan untrusted remote skills in a constrained workspace and avoid using the optional policy or pre-commit controls unless they match the intended workflow. <br>
Risk: The optional AGENTS.md policy and pre-commit hook can affect ongoing agent or repository behavior. <br>
Mitigation: Add these controls only after reviewing the examples and confirming that persistent scanning gates are desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vincentchan/claw-skill-guard) <br>
- [1Password research on agent skill attack surface](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text reports and Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Risk findings are advisory and grouped by critical, high, medium, low, or safe status.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

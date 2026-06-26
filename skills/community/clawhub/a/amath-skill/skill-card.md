## Description: <br>
Discover the Socthink 奥数 learning system through curriculum trees, topic/problem lookup, Socratic tutoring, and quiz flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[star8592](https://clawhub.ai/user/star8592) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, developers, and AI workflow builders use this skill to explore Socthink's guided math-learning product through curriculum discovery, problem lookup, Socratic tutoring, and quiz practice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Socthink services and may handle account credentials or bearer tokens for authenticated flows. <br>
Mitigation: Use intended Socthink accounts only, prefer explicit per-command tokens where practical, and avoid storing long-lived tokens in .env files on shared machines. <br>
Risk: Installer and helper scripts execute shell commands during setup and use. <br>
Mitigation: Review the bundled scripts and the documented OpenClaw installer before running them, especially when using curl piped to bash. <br>
Risk: Quiz and tutoring behavior depends on remote Socthink API responses and authenticated session state. <br>
Mitigation: Preserve returned IDs exactly, report API errors faithfully, and verify authenticated actions with the intended user token. <br>


## Reference(s): <br>
- [Socthink homepage](https://amath.socthink.cn) <br>
- [ClawHub skill page](https://clawhub.ai/star8592/amath-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/star8592) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from the Socthink API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves returned identifiers and reports API error payloads faithfully.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

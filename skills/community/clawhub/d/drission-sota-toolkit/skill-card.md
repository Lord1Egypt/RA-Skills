## Description: <br>
Professional Web Intelligence & Automation Toolkit. Features Protocol Phantom (TLS/JA4), Local Socket Relaying, and Hardened physical gating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Biogod2020](https://clawhub.ai/user/Biogod2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external automation operators use this skill for local browser-based web intelligence, search aggregation, Chrome/CDP control, and gated local relay workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact local Chrome/CDP control and anti-bot automation may affect logged-in browser sessions or protected third-party services. <br>
Mitigation: Run only in an isolated VM or container with a disposable, non-logged-in browser profile, and use it only against services where you have authorization. <br>
Risk: Declared metadata is partly inconsistent with the bundled high-risk browser and relay capabilities. <br>
Mitigation: Require publisher metadata alignment and human review before deployment, including explicit per-action confirmation and allowlists for sensitive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Biogod2020/drission-sota-toolkit) <br>
- [Security explanation](artifact/SECURITY_EXPLAINED.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance, terminal output, Python code, configuration snippets, and local JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local Chrome, Xvfb/dbus launch support, and declared Python packages for browser automation workflows.] <br>

## Skill Version(s): <br>
7.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

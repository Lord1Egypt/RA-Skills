## Description: <br>
Picoclaw runtime traffic monitoring baseline for lightweight AI gateway proxy inspection, egress detection, and posture integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Builders and security operators use this skill as a Picoclaw landing zone for opt-in runtime traffic monitoring, including proxy inspection planning, exfiltration and injection detection design, redacted local findings, and posture export for Picoclaw security profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future proxy inspection, HTTPS MITM, local threat logs, and profile export are sensitive capabilities. <br>
Mitigation: Keep monitoring opt-in, process-scoped, redacted, and operator-controlled before enabling any future implementation. <br>
Risk: The published artifact is a scaffold and does not provide active runtime monitoring or blocking. <br>
Mitigation: Treat it as an implementation baseline and review added runtime code, tests, and configuration before relying on detection outcomes. <br>
Risk: Standalone installs can be exposed to release artifact tampering if checksums and signatures are skipped. <br>
Mitigation: Verify the signed release manifest, archive checksum, SKILL.md, and skill.json before installing or extracting standalone artifacts. <br>


## Reference(s): <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-picoclaw-traffic-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON schemas and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spec baseline only; this release does not include active proxy or runtime implementation code.] <br>

## Skill Version(s): <br>
0.0.1-beta5 (source: artifact/SKILL.md, artifact/skill.json, artifact/CHANGELOG.md, released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

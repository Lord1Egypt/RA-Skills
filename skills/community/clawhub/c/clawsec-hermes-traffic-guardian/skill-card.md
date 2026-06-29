## Description: <br>
Hermes runtime traffic monitoring baseline for opt-in proxy inspection, egress detection, and attestation-aware traffic posture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill as a specification baseline for opt-in Hermes traffic monitoring, including planned proxy inspection, exfiltration and injection detection, redacted local findings, and posture export for attestation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future proxy or HTTPS inspection behavior could expose sensitive request data if configured too broadly. <br>
Mitigation: Keep monitoring opt-in, scope proxy settings per process, require operator-supplied CA trust for HTTPS inspection, bound scanned content, and redact snippets before logs or attestation-linked outputs. <br>
Risk: This release is a specification scaffold and does not include active traffic-monitoring runtime code. <br>
Mitigation: Treat the package as implementation guidance, and review future runtime code for proxy behavior, CA trust handling, log redaction, and background-mode behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-hermes-traffic-guardian) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [Hermes Traffic Guardian Specification](SPEC.md) <br>
- [Hermes Traffic Guardian README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON schemas] <br>
**Output Format:** [Markdown with shell command examples and JSON schema snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Specification-only release; no active proxy or runtime implementation is included.] <br>

## Skill Version(s): <br>
0.0.1-beta5 (source: server release evidence, frontmatter, skill.json, and changelog, released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

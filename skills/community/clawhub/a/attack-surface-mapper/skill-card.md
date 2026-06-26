## Description: <br>
Purple team - map an agent's full attack surface by combining red team probes and blue team detections, then identify defense coverage gaps and prioritize hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arhadnane](https://clawhub.ai/user/arhadnane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and agent operators use this skill to review agent attack surfaces, compare red team test coverage with blue team detections, and produce a prioritized hardening plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local security posture reports may expose defensive gaps if shared or committed. <br>
Mitigation: Keep .security/surface-map private, avoid committing generated reports, and review output before sharing. <br>
Risk: Hardening recommendations are advisory and may be incomplete when security logs or audit reports are missing or stale. <br>
Mitigation: Review recommendations before changing defenses and rerun the map after configuration, skill, or detection changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arhadnane/attack-surface-mapper) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance, Files] <br>
**Output Format:** [JSON and Markdown security posture reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local reports under .security/surface-map and can list known attack surface categories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Handle cybersecurity triage, threat modeling, secure reviews, and incident reporting with strict authorization and evidence discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security practitioners, and leaders use this skill for authorized incident triage, threat modeling, secure design review, vulnerability prioritization, tabletop preparation, and risk reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive security context could be stored in local notes. <br>
Mitigation: Keep ~/cybersecurity/ private, avoid storing secrets, tokens, private keys, or raw sensitive logs, and periodically clear stale incident notes. <br>
Risk: Cybersecurity requests can drift into unauthorized or harmful activity. <br>
Mitigation: Require clear authorization and scope before offensive or high-risk work, and use safe alternatives such as local labs, tabletop analysis, detection logic, or remediation planning when scope is unclear. <br>
Risk: Incident response recommendations can disrupt systems or destroy useful evidence. <br>
Mitigation: Preserve logs, timestamps, affected hosts, and symptoms before disruptive containment, and flag actions that are irreversible, noisy, or likely to hinder investigation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/cybersecurity) <br>
- [Skill homepage](https://clawic.com/skills/cybersecurity) <br>
- [Setup guide](setup.md) <br>
- [Threat modeling workflow](threat-modeling.md) <br>
- [Incident triage flow](triage.md) <br>
- [Reporting structure](reporting.md) <br>
- [Safety boundaries](safety-boundaries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured analysis, recommendations, and occasional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initialize or update local context files under ~/cybersecurity/ when setup or memory support is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

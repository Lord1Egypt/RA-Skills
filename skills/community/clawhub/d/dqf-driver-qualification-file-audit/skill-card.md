## Description: <br>
Use this skill when a motor-carrier safety director, DOT compliance manager, or third-party DQF administrator needs a pre-audit review of FMCSA Driver Qualification Files under 49 CFR § 391. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Motor-carrier safety directors, DOT compliance managers, third-party DQF administrators, and HR safety staff use this skill to produce draft Driver Qualification File audit findings, prioritized remediation, fleet-level rollups, and DER sign-off support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews sensitive employee compliance records and may involve driver identifiers or medical-certification context. <br>
Mitigation: Use internal IDs and last-4 CDL only, keep source records in the carrier-controlled DQF system, and avoid pasting full CDL numbers, SSNs, full addresses, or medical-record content into agent working notes. <br>
Risk: Draft findings could be mistaken for legal advice, medical fitness determinations, official FMCSA submissions, or dispatch authorization. <br>
Mitigation: Treat outputs as draft audit support requiring DOT-designated employer representative, compliance, legal, and appropriate medical-examiner review before acting on them as compliance records. <br>
Risk: Users may expect the agent to query or update external compliance systems. <br>
Mitigation: Use the skill to document required evidence only; do not have the agent log into, query, file with, or alter records in FMCSA, Clearinghouse, CDLIS, DMV, National Registry, TPR, or carrier systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/dqf-driver-qualification-file-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown draft audit packet with per-driver findings tables, remediation lists, fleet rollup, cited-regulation appendix, unresolved information, and DER sign-off block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are draft compliance-review support and should use internal driver IDs and last-4 CDL only.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and CHANGELOG, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

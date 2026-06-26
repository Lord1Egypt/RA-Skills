## Description: <br>
Review computer-vision experiment reproducibility evidence, dataset readiness, metric gates, and launch risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data scientists, and release reviewers use this skill to assess whether a computer-vision experiment, report, or launch claim has enough reproducibility evidence to share or promote. It focuses on dataset readiness, metric gates, privacy risks, leakage risks, and the smallest next verification step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include credentials, account details, private paths, internal notes, or confidential dataset contents in evidence shared for review. <br>
Mitigation: Ask users to redact sensitive material unless they intentionally want it considered in the current conversation. <br>
Risk: Computer-vision claims involving medical, biometric, face, child-safety, or surveillance-adjacent use cases can require stronger evidence before promotion. <br>
Mitigation: Treat those claims as high-risk and require stronger reproducibility, privacy, leakage, and policy evidence before returning a promotable verdict. <br>
Risk: The skill provides advisory reproducibility review and can miss issues when evidence is incomplete or claims are unverified. <br>
Mitigation: Separate completed-run evidence from unverified claims and return the smallest next check needed to improve confidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/data-science-cv-repro-lab) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zack-dev-cm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review with sections for experiment, evidence, risks, verification, and verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Verdict is one of reproducible, reproducible_with_notes, blocked, or do_not_promote.] <br>

## Skill Version(s): <br>
1.9.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

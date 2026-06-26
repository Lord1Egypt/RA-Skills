## Description: <br>
Diagnoses Ocean Engine and Tencent Ads advertising plans from user-provided platform, account, and ad identifiers, then turns API or rules-based findings into actionable optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suwangsen](https://clawhub.ai/user/suwangsen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Performance marketers and advertising operations teams use this skill to diagnose low delivery, high cost, and other campaign-plan issues for Ocean Engine or Tencent Ads. The agent collects required identifiers, runs the provided diagnostic script, and summarizes the resulting recommendations in a human-readable report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagnostic script queries advertising accounts using locally configured Ocean Engine or Tencent Ads access tokens. <br>
Mitigation: Keep .env private, use least-privileged and short-lived tokens where possible, and avoid exposing full request URLs or tokens in logs. <br>
Risk: Incorrect account or ad identifiers could query the wrong advertising data and produce misleading recommendations. <br>
Mitigation: Confirm the platform, account ID, and ad ID with the user before running the diagnostic command. <br>
Risk: Dependency ranges are not pinned exactly in requirements.txt. <br>
Mitigation: Pin and review dependency versions in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suwangsen/adv-plan-diagnosis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and JSON result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to provide platform, account ID, ad ID, and for Tencent Ads an optional target cost; API tokens are read from a local .env file.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata, created 2026-05-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

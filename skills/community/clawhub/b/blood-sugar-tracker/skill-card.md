## Description: <br>
Tracks blood sugar readings, analyzes trends, suggests diet adjustments, and surfaces abnormal value alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to record blood sugar readings, review trends, request diet suggestions, and configure abnormal-value alerts from documented CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health-related ranges and diet suggestions could be mistaken for medical advice. <br>
Mitigation: Use outputs as tracking support only, and direct users to qualified medical professionals for diagnosis, treatment, medication, or urgent-care decisions. <br>
Risk: Server security evidence marks the release suspicious because an autoreview helper can grant nested review broad local access by default. <br>
Mitigation: Review before installing and follow the evidence guidance to run autoreview with `--no-yolo` or `AUTOREVIEW_YOLO=0` unless bypassing prompts is intentional. <br>
Risk: The artifact declares `curl` as a required binary and documents shell commands. <br>
Mitigation: Run commands in a trusted environment, inspect generated shell commands before execution, and avoid passing sensitive health data to untrusted endpoints. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaising-openclaw1/blood-sugar-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/kaising-openclaw1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health-range summaries and diet suggestions; outputs should not be treated as medical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

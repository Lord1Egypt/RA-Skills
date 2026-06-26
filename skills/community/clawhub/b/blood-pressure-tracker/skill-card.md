## Description: <br>
Blood Pressure Tracker records blood pressure readings, analyzes trends, offers health suggestions, alerts on abnormal values, and generates statistical reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to track systolic and diastolic blood pressure readings, review trends over time, receive non-medical tips, configure alert thresholds, and produce summary reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data. <br>
Mitigation: Confirm where blood pressure readings are stored, how they can be deleted, and whether storage meets the user's privacy requirements before entering personal health data. <br>
Risk: Automated health suggestions may be incomplete or misleading. <br>
Mitigation: Treat generated tips as tracking support only and consult qualified medical professionals for diagnosis, treatment, or urgent health decisions. <br>
Risk: The package declares a curl dependency, which may imply network behavior. <br>
Mitigation: Review why curl is required and verify expected network access before using the skill in restricted or privacy-sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/blood-pressure-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kaising-openclaw1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health suggestions, alerts, trend summaries, and statistical reports; automated tips should not be treated as medical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

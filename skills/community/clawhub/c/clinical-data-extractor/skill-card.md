## Description: <br>
Extract clinical trial data from pharmaceutical conference websites or PDF documents into structured Markdown reports with drug, manufacturer, indication, phase, trial, conference, efficacy, and safety data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abinww](https://clawhub.ai/user/abinww) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and clinical research teams use this skill to extract structured clinical trial information from URLs or PDFs and produce standardized Markdown reports with efficacy, safety, and expert commentary sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive clinical documents or untrusted URLs. <br>
Mitigation: Use it only with documents and URLs the user is allowed to process, and review extracted content before relying on it. <br>
Risk: PDF workflows mention an edit-capable extraction tool. <br>
Mitigation: Prefer local, read-only PDF extraction when possible and confirm tool behavior before using edit-capable actions. <br>
Risk: Generated Markdown files are written to a configured workspace path. <br>
Mitigation: Confirm the configured output directory before running the skill, especially when handling clinical or proprietary material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abinww/clinical-data-extractor) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Text, Guidance] <br>
**Output Format:** [Markdown report with structured tables and optional image references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports using the configured output path and filename format.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Analyzes a user's Fulcra evening debriefs and morning check-ins to relate meeting load to day ratings and recommend a confidence-gated meeting cadence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keng009](https://clawhub.ai/user/keng009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and their agents use this skill during weekly schedule reviews or overbooking questions to analyze logged meeting counts, day ratings, and cadence feedback. It helps the agent present only returned metrics, identify a likely meeting sweet spot, and suggest a small number of scheduling changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes tools beyond the stated meeting-cadence task that can access or modify unrelated Fulcra and Attio CRM data. <br>
Mitigation: Review the shipped scripts before installation, run in a trusted environment, and expose only credentials needed for the intended cadence analysis. <br>
Risk: Providing Attio credentials can enable unrelated CRM operations bundled with the package. <br>
Mitigation: Do not set ATTIO_API_KEY unless those CRM utilities are intentionally needed and approved. <br>
Risk: Cadence analysis uses personal meeting patterns, day ratings, and check-in history. <br>
Mitigation: Keep outputs private, avoid public disclosure of personal metrics, and use dry-run or read-only analysis before saving annotations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON analysis from the script, with concise Markdown guidance and optional shell commands for direct execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Confidence-gated output based on available debrief history; optional save mode writes a Fulcra Cadence Analysis annotation after preview or dry run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

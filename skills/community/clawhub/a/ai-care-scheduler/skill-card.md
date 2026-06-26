## Description: <br>
通过对话即可完成养老机构护理排班，简单快捷。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnspica](https://clawhub.ai/user/cnspica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Care-facility operators and scheduling staff use this skill to collect staff names, shift limits, cycle length, and start date through conversation, then generate a nursing schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AI mode can send staff names and scheduling rules to DashScope when a user provides an API key. <br>
Mitigation: Use local mode by leaving the API key blank unless third-party processing is approved for the staff data being scheduled. <br>
Risk: CSV exports contain personnel and shift information. <br>
Mitigation: Treat exported CSV files as sensitive staffing data and store or share them only in approved locations. <br>
Risk: Generated schedules may not reflect every real-world staffing constraint or labor policy. <br>
Mitigation: Review generated rosters before operational use and adjust assignments for local policy, coverage, and worker availability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnspica/ai-care-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, code, guidance] <br>
**Output Format:** [Markdown schedule table with optional CSV file export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include dates, shifts, shift times, assigned staff names, and optional local CSV exports; optional AI mode may use DashScope when the user provides an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

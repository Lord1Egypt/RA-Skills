## Description: <br>
Stay ahead of EPA enforcement at cement plants with NESHAP Subpart LLL limits, CEMS QA/QC, Title V permits, alternative fuels emissions, exceedance response, and NOV defense procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larkinjoshuad](https://clawhub.ai/user/larkinjoshuad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External cement plant environmental managers, compliance officers, plant managers, and CEMS technicians use this skill to interpret federal cement emissions requirements, troubleshoot CEMS and exceedance events, assess reporting obligations, and prepare enforcement response guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides environmental compliance guidance that could be mistaken for a final legal or reporting determination. <br>
Mitigation: Treat outputs as conservative prompts to investigate and confirm obligations against the facility Title V permit, state requirements, official regulations, and qualified environmental counsel before acting. <br>
Risk: Federal knowledge bases may not cover stricter state, local, or site-specific permit conditions. <br>
Mitigation: Verify any recommendation against the applicable permit, state agency requirements, and current official regulatory text. <br>
Risk: CEMS work, stack testing, and emission-control maintenance can involve toxic gases, fall hazards, confined spaces, and chemical exposure. <br>
Mitigation: Follow the safety guidance in the skill's environmental safety reference, use required PPE and work permits, and involve qualified site safety personnel before field work. <br>
Risk: The reporting checker intentionally favors conservative reporting behavior and may over-trigger obligations for ambiguous event descriptions. <br>
Mitigation: Use checker output to prioritize timely review, then document the event facts and confirm final reportability with the environmental compliance officer and permitting authority. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/larkinjoshuad/cementops-environmental-compliance) <br>
- [CementOps AI](https://cementops.ai) <br>
- [Cement Kiln Emissions Regulations](knowledge-bases/cement-kiln-emissions.json) <br>
- [CEMS Requirements](knowledge-bases/cems-requirements.json) <br>
- [Title V Permits](knowledge-bases/title-v-permits.json) <br>
- [Alternative Fuels Emissions Impact](knowledge-bases/alternative-fuels-emissions.json) <br>
- [Startup, Shutdown, and Bypass Compliance](knowledge-bases/startup-shutdown-bypass.json) <br>
- [Environmental Reporting Obligation Rules](reporting-rules.json) <br>
- [NOV Response Guide](guidance-templates/nov-response-guide.md) <br>
- [Environmental Compliance Safety Hazards](safety/environmental-safety.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with regulatory references, ordered response steps, and inline shell commands when the reporting checker is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local reference data and a deterministic reporting checker for described environmental events; state and facility-specific permit terms still require user verification.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Parses job description text into structured position details including title, requirements, salary range, company information, skills, responsibilities, and keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[51mee-com](https://clawhub.ai/user/51mee-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, HR teams, and developers use this skill to convert job descriptions into structured position data for review, search, or downstream workflow inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated position data may be incomplete or unreliable when job descriptions are sparse, ambiguous, or untrusted. <br>
Mitigation: Validate the returned JSON before using it in hiring, analytics, or business workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/51mee-com/51mee-position-parse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON object following the PositionInfo interface, with an optional Markdown report layout documented by the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Missing fields should be returned as null; validate generated JSON before using it in automated workflows.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

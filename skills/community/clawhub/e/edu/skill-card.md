## Description: <br>
Aggregates 28 education-focused subskills and routes teacher or student learning requests to matching tools with a unified response format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenleimap](https://clawhub.ai/user/chenleimap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, students, and education support staff use this skill to route education, study, exam preparation, lesson planning, assignment, and subject-learning requests to appropriate education subskills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad education trigger keywords may activate the router more often than intended. <br>
Mitigation: Confirm the user's intent and the selected education subskill before relying on the response. <br>
Risk: Requests involving assignments, grades, LMS records, calendars, or student information may expose sensitive education data to downstream subskills. <br>
Mitigation: Review the selected subskill before sharing sensitive data and limit inputs to what the task requires. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenleimap/edu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured text or Markdown responses from routed education subskills] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code in the artifact; downstream behavior depends on the selected subskill.] <br>

## Skill Version(s): <br>
v1.0.9-simplified (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

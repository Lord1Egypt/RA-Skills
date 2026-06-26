## Description: <br>
Access Canvas LMS (Instructure) for course data, assignments, grades, and submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pranavkarthik10](https://clawhub.ai/user/pranavkarthik10) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students, instructors, and education-support agents use this skill to retrieve Canvas course information, assignments, due dates, grades, submissions, files, modules, announcements, discussions, and inbox messages through the Canvas REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may access educational records such as grades, submissions, messages, and course files using the user's Canvas API token. <br>
Mitigation: Verify CANVAS_URL points to the correct school Canvas domain, keep CANVAS_TOKEN out of shared logs and committed files, minimize sensitive queries, and revoke the token when it is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and Canvas REST API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided CANVAS_TOKEN and CANVAS_URL; API responses may include educational records and other sensitive Canvas data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

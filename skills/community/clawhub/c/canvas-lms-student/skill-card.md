## Description: <br>
Use when the user needs to interact with Canvas LMS as a student, with read-only access to courses, assignments, files, and deadlines for academic workflows including assignment research, deadline tracking, and material gathering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efan404](https://clawhub.ai/user/efan404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and agents acting on a student's behalf use this skill to inspect Canvas LMS courses, assignments, files, deadlines, grades, and announcements. It is intended for read-only academic planning, material collection, calendar export, and assignment context gathering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Canvas API token that can grant access to private course data. <br>
Mitigation: Treat CANVAS_API_TOKEN like a password, keep environment variables and config files private, and install the skill only when agent access to Canvas is intended. <br>
Risk: Broad prompts may cause the agent to query or summarize more Canvas content than the user intended. <br>
Mitigation: Use specific prompts that name the course, assignment, file type, or deadline range needed for the task. <br>
Risk: Downloaded course materials and calendar exports may contain private academic information. <br>
Mitigation: Choose trusted local output folders and avoid sharing generated files unless they have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/efan404/canvas-lms-student) <br>
- [Project homepage](https://github.com/Efan404/canvas-lms-student-skill) <br>
- [API Overview](references/api-overview.md) <br>
- [Courses](references/courses.md) <br>
- [Assignments](references/assignments.md) <br>
- [Files](references/files.md) <br>
- [Calendar Export](references/calendar-export.md) <br>
- [Search](references/search.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON from helper scripts, and generated local files such as downloaded course materials or iCalendar exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Canvas base URL and API token through environment variables or a local config file; file download and calendar export tools can write to local output paths.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter, manifest, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

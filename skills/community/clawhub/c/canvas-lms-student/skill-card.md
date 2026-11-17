## Description:

The Canvas LMS Student Skill lets agents retrieve a student's Canvas courses, assignments, files, deadlines, grades, and related course content for academic workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efan404](https://clawhub.ai/user/efan404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and students use this skill to let an agent check Canvas coursework, gather assignment requirements, find course materials, export deadlines, and summarize course status from read-only Canvas API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canvas API tokens can access private course information and may be stored in plaintext when the config-file method is used.

Mitigation: Prefer environment variables or a secure secret store, use the narrowest practical Canvas token scope, and avoid storing tokens on shared machines.

Risk: The file-download workflow can expose the Canvas token or write files outside the selected output folder.

Mitigation: Avoid the download feature until the token-forwarding and path-traversal issues are fixed; when testing, use trusted Canvas URLs, explicit output folders, and a sandboxed working directory.

Risk: The assignment-detail workflow can support essay-generation behavior that may conflict with school academic-integrity rules.

Mitigation: Use gathered assignment details to understand requirements and plan work, and require users to follow their institution's academic-integrity policy before generating or submitting coursework.

Risk: Calendar exports and downloaded materials write private course data to local files.

Mitigation: Review output paths before running, inspect generated files before importing or sharing them, and delete local exports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/efan404/skills/canvas-lms-student)
- [ClawHub metadata homepage](https://github.com/Efan404/canvas-lms-student-skill)
- [API Overview](references/api-overview.md)
- [Courses](references/courses.md)
- [Assignments](references/assignments.md)
- [Files](references/files.md)
- [Calendar Export](references/calendar-export.md)
- [Search](references/search.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration guidance]

**Output Format:** [Markdown, JSON, local files, and iCalendar (.ics) files, depending on the selected Canvas workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CANVAS_BASE_URL and CANVAS_API_TOKEN or a local Canvas config file; can write course-material downloads and calendar exports to local paths.]

## Skill Version(s):

0.1.1 (source: frontmatter, manifest, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

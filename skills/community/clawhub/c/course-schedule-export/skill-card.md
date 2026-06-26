## Description: <br>
Turn school or university timetables into checked .ics calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Davidai-1999](https://clawhub.ai/user/Davidai-1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, school staff, and agents assisting them use this skill to normalize timetable sources, resolve schedule ambiguity, verify coverage against source entries, and generate a local .ics calendar export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated calendars can be wrong if timezone, week-1 anchor dates, period times, or odd/even week rules are missing or ambiguous. <br>
Mitigation: Require those inputs before export, mark unresolved schedule items for confirmation, and verify the manifest against source entries before generating the .ics file. <br>
Risk: Class schedules may contain private location, attendance, or routine details. <br>
Mitigation: Process only timetable files and output paths the user intends to use, and avoid sharing generated manifests or .ics files beyond the intended calendar workflow. <br>
Risk: The skill can run included local Python scripts and write a calendar file. <br>
Mitigation: Review the manifest and selected output path before running the scripts, and use the included coverage checker to catch dropped or unsupported schedule entries. <br>


## Reference(s): <br>
- [Manifest Schema](references/manifest-schema.md) <br>
- [Coverage Schema](references/coverage-schema.md) <br>
- [Pitfalls](references/pitfalls.md) <br>
- [Course Schedule Export Release](https://clawhub.ai/Davidai-1999/course-schedule-export) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance, JSON schedule manifests, shell commands, and local .ics files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The export path writes a local .ics file from a normalized manifest and reports the output path and event count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

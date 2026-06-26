## Description: <br>
Provides systematic C/C++ debugging checklists and helper functions for common issues such as null pointers, memory leaks, race conditions, boundary errors, and uninitialized variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gatsby047-oss](https://clawhub.ai/user/gatsby047-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and code reviewers use this skill as lightweight C/C++ debugging guidance for checking common bug classes and reinforcing systematic review habits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checklist guidance and helper functions can miss issues or give incomplete debugging advice. <br>
Mitigation: Treat the skill as guidance only and verify results with compiler warnings, sanitizers, Valgrind, static analysis, tests, and code review. <br>
Risk: Adding the C/C++ header to a project can change build behavior or runtime diagnostic output. <br>
Mitigation: Review the header and test it in a controlled environment before relying on it in production code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gatsby047-oss/debug-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown guidance with C/C++ examples and checklist text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output; validate findings with compiler warnings, sanitizers, Valgrind, static analysis, tests, and code review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Reviews staged code changes for production readiness, error handling, code quality, and unit test coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaseenkadlemakki](https://clawhub.ai/user/yaseenkadlemakki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to have an agent review staged code changes, identify production-readiness issues, and propose fixes or tests before committing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest or generate code fixes and tests that may change repository behavior. <br>
Mitigation: Review generated changes, run tests, and inspect diffs before applying or committing. <br>
Risk: The review may require sharing staged repository diffs with the agent. <br>
Mitigation: Use only on repositories and changes you intend to expose to the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yaseenkadlemakki/code-review-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review comments with code snippets, suggested fixes, and test implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository changes and tests; users should review generated changes before applying or committing them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Write and evaluate effective Python tests using pytest, including test design, fixtures, parameterization, mocking, and async testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to write, review, debug, and improve Python pytest coverage with clear test structure, fixture usage, mocking boundaries, async testing conventions, and project-specific pytest commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested pytest or snapshot-update commands may execute project test code or modify snapshot files when a user chooses to run them. <br>
Mitigation: Review commands before running them, execute them in the intended project environment, and treat snapshot updates as code changes. <br>
Risk: Project-specific assumptions may not match every repository. <br>
Mitigation: Confirm the project uses the assumed tools and conventions, including uv, pytest-xdist, inline-snapshot, FastMCP, and asyncio_mode='auto', before applying the guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/fix-build-agentops-testing-python) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pytest test patterns, fixture examples, async testing guidance, and uv/pytest command suggestions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

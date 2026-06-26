## Description: <br>
Detect, diagnose, and fix flaky tests by analyzing CI history, timing-sensitive behavior, shared state, race conditions, and environment dependencies, then proposing targeted fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate intermittent test failures in CI and local test runs, classify likely causes, and produce fix, quarantine, or stability-report guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may inspect CI history, download test artifacts, or run test suites in the active repository. <br>
Mitigation: Run only in the intended repository, review commands before execution, and treat downloaded CI artifacts as potentially sensitive. <br>
Risk: Generated fixes, skips, or quarantine changes may hide product defects or reduce test coverage if applied unreviewed. <br>
Mitigation: Require code review and stable verification before committing generated changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose test fixes, quarantine changes, and reports; review before execution or commit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

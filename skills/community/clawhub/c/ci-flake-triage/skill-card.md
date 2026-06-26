## Description: <br>
Detect flaky tests from JUnit XML retries and emit a triage report with top unstable cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze JUnit XML retry artifacts, identify flaky candidates, and separate persistent failures from transient test instability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad JUNIT_GLOB patterns may include private CI logs or unrelated test artifacts in the analysis output. <br>
Mitigation: Scope JUNIT_GLOB to the intended test-results directory and review generated reports before sharing them. <br>
Risk: Enabling fail gates can make CI jobs exit non-zero when persistent failures or flaky candidates are present. <br>
Mitigation: Use the default reporting-only mode first, then enable FAIL_ON_PERSISTENT or FAIL_ON_FLAKE deliberately in CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/ci-flake-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain-text or JSON triage report with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local JUnit XML files matched by JUNIT_GLOB and can optionally exit non-zero when persistent failures or flaky candidates are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

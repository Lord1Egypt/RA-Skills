## Description:

Design and implement adaptive testing systems using Item Response Theory (IRT) for computerized adaptive tests, psychometric assessment, ability estimation, question calibration, test design, and IRT models (1PL/2PL/3PL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodstocksoftware](https://clawhub.ai/user/woodstocksoftware)

### License/Terms of Use:


## Use Case:

Developers, psychometricians, assessment teams, and educators use this skill to design computerized adaptive tests, select IRT models, calibrate item banks, choose stopping rules, and implement CAT workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implementation guidance includes production-style API patterns for test scoring and session control that may be insecure if copied directly.

Mitigation: Treat the API example as conceptual only and add authenticated users, session ownership checks, protected server-side answer scoring, current-question enforcement, replay protection, and tests for forged submissions before production use.

Risk: Adaptive testing designs can produce inaccurate placement or assessment results if item calibration, exposure control, or simulation validation is skipped.

Mitigation: Validate IRT parameters, enforce item exposure controls, simulate test sessions across the target ability range, and review calibration quality before operational deployment.

## Reference(s):

- [Item Calibration Guide](references/calibration.md)
- [CAT Implementation Guide](references/implementation.md)
- [catsim documentation](https://douglasrizzo.github.io/catsim/)
- [IRT in Python tutorial](https://irt.psychometricsociety.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code examples and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conceptual psychometrics guidance, IRT formulas, API patterns, database schema examples, and test validation checklists.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

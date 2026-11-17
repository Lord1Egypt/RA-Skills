## Description:

You are a performance testing expert with expertise in load testing, stress testing, performance monitoring, and optimization strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design load tests, stress tests, performance monitoring, capacity planning, CI/CD performance gates, and optimization recommendations for applications, databases, and infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated load, stress, checkout, or database benchmark examples can create heavy traffic or modify systems if copied into real environments without controls.

Mitigation: Run tests only against systems the user owns or is explicitly authorized to test, preferably isolated staging environments with synthetic data.

Risk: Examples may lack enough traffic limits, stop conditions, non-production defaults, least-privilege credentials, dependency pinning, and safer package installation steps for automation.

Mitigation: Add explicit rate limits, thresholds, stop conditions, non-production targets, least-privilege database credentials, pinned CI dependencies, and reviewed installation steps before automation.

Risk: Performance recommendations or generated scripts may be incorrect for a specific architecture, data profile, or service-level objective.

Mitigation: Review generated tests and recommendations with application owners, validate them in a controlled environment, and compare results against known baselines before deployment.

## Reference(s):

- [Performance Tester Code Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-performance-tester)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include load-test scripts, database benchmark commands, CI/CD snippets, monitoring configurations, performance budgets, reports, and optimization recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

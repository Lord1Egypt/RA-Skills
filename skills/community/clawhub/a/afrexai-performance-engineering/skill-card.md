## Description:

Complete performance engineering system for profiling, optimization, load testing, capacity planning, and performance culture across applications, APIs, databases, and frontend systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to diagnose slow applications, design profiling and load-testing workflows, interpret results, recommend optimizations, plan capacity, and add performance checks to CI/CD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples may run unpinned external tools such as `npx` packages.

Mitigation: Review commands before execution and use pinned, locally locked, or preapproved tool versions in sensitive projects.

Risk: Profiling examples can expose diagnostic endpoints or runtime internals.

Mitigation: Bind profiling servers to loopback, add access controls, and avoid exposing diagnostic interfaces on public networks.

Risk: Load-testing guidance can disrupt systems or third-party services if run against unauthorized targets.

Mitigation: Run load tests only against systems you own or are authorized to test, preferably in staging.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/1kalin/skills/afrexai-performance-engineering)
- [async-profiler](https://github.com/async-profiler/async-profiler)
- [AfrexAI context packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with templates, checklists, code blocks, command examples, and interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include performance budgets, profiling plans, load-test templates, diagnostic checklists, capacity models, and CI/CD gate recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

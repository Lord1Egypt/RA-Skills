## Description:

Autonomous quality engineering swarm for continuous behavioral verification, exhaustive E2E testing, self-healing fix loops, DDD/ADR/TDD workflows, BDD/Gherkin specifications, quality gates, defect prediction, chaos testing, and cross-context dependency awareness across common application architectures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikennaokpala](https://clawhub.ai/user/ikennaokpala)

### License/Terms of Use:

MIT

## Use Case:

Developers and quality engineers use Forge to run autonomous behavioral verification, end-to-end testing, quality gates, and self-healing fix loops across application architectures such as monoliths, microservices, monorepos, and mobile-backend systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run project commands, start background services, modify code, and create commits during autonomous workflows.

Mitigation: Use a disposable branch or isolated test environment, and supervise auto-fix and auto-commit modes before accepting changes.

Risk: Project configuration can direct the agent toward migrations, seeding, backend targets, and other environment-sensitive actions.

Mitigation: Review forge.config.yaml, .env files, and backend targets before execution, and verify they point only to non-production systems.

Risk: External tooling invoked with floating versions can change behavior between runs.

Mitigation: Pin or preinstall required external tooling instead of relying on @latest during execution.

Risk: Persistent memory reuse can carry learned fix patterns or project state across runs.

Mitigation: Disable or closely supervise persistent memory reuse when testing untrusted codebases or sensitive projects.

## Reference(s):

- [Forge ClawHub skill page](https://clawhub.ai/ikennaokpala/skills/forge)
- [Continuous Behavioral Verification: Ongoing Path to Done](https://www.linkedin.com/pulse/continuous-behavioral-verification-ongoing-path-done-ikenna-okpala)
- [Build with Quality Skill: How I Build Software 10x Faster](https://www.linkedin.com/pulse/build-quality-skill-how-i-build-software-10x-faster-mondweep-chakravorty)
- [claude-code-v3-qe-skill](https://github.com/mondweep/vibe-cast)
- [agentic-qe](https://github.com/proffesor-for-testing/agentic-qe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, configuration snippets, and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify project files, run tests, launch local services, persist learned patterns, and create local commits when invoked in autonomous modes.]

## Skill Version(s):

1.0.0 (source: release evidence and CHANGELOG, released 2026-02-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

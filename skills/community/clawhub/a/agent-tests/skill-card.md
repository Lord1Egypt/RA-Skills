## Description:

Agent Tests helps define, run, and track agent behavior tests with assertions, regression tracking, and performance benchmarking without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create JSON-backed behavior tests, run assertions, track regressions, and benchmark agent workflows during skill or model changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local JSON-backed tests and results can retain secrets, private prompts, or sensitive model outputs on disk.

Mitigation: Do not store secrets, private prompts, or sensitive model outputs in tests unless local retention is acceptable; review or delete generated data when needed.

Risk: Current test runs simulate agent output rather than executing a real agent.

Mitigation: Treat results as a testing scaffold and verify critical behavior against real agent execution before relying on pass/fail outcomes.

Risk: Test definitions, results, and benchmark history are written to local JSON files.

Mitigation: Use a controlled data directory such as --dir or TEST_DIR for isolated runs, and review generated files before sharing a workspace.

## Reference(s):

- [Agent Tests README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/jlacroix82/skills/agent-tests)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-backed test definitions and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON test definitions, result history, and benchmark history under memory/agent-tests by default; current test runs simulate agent output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

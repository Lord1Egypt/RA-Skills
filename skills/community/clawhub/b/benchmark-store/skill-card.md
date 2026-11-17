## Description:

Benchmark Store helps agents initialize benchmark databases, compare skill scores against frozen baselines, inspect Pareto-front regressions, and consult skill evaluation standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to maintain skill benchmark data, compare candidate scores against historical baselines, detect Pareto-front regressions, and consult quality tier standards. It supports benchmark storage and regression context rather than candidate scoring or automated skill improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes untrusted execution paths with weak containment.

Mitigation: Install and run it only in a controlled benchmark environment with enforced sandboxing and timeouts.

Risk: Hidden-test handling should not be treated as trusted for protected evaluations.

Mitigation: Use it for trusted hidden tests only after vetted authenticated encryption is in place.

Risk: Benchmark scoring and deletion behavior can affect baselines and leaderboard data.

Mitigation: Review scoring and deletion actions before use, keep database backups, and require documented evaluator inputs for comparisons.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/benchmark-store)
- [Publisher Profile](https://clawhub.ai/user/lanyasheng)
- [Benchmark Database](artifact/data/benchmark-database.md)
- [Evaluation Standards](artifact/data/evaluation-standards.md)
- [Red Team Guide](artifact/data/red-team-guide.md)
- [Test Cases](artifact/data/test-cases.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command snippets, Python code examples, JSON comparison outputs, and SQLite benchmark records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update benchmark database entries, leaderboard data, and Pareto regression reports.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Eval Skills is a framework-agnostic toolkit for discovering, scaffolding, selecting, evaluating, and reporting on AI agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[islinxu](https://clawhub.ai/user/islinxu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to evaluate individual AI skills before deployment, compare candidate skills on shared benchmarks, enforce CI/CD quality gates, and generate evaluation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluated local skills, MCP stdio servers, and custom scorer files may run with more host access than expected.

Mitigation: Use Docker mode on a hardened runner without sensitive credentials, and treat evaluated code and custom scorers as trusted code unless strong isolation is enforced.

Risk: Untrusted benchmarks that reference custom scorer files can introduce code execution risk.

Mitigation: Avoid untrusted benchmarks with customScorerPath, and do not run third-party skills on workstations or CI accounts with broad secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/islinxu/skills/eval-skills)
- [README](README.md)
- [Quick Start Guide](docs/guides/quickstart.md)
- [Creating a Custom Skill](docs/guides/create-skill.md)
- [Creating a Custom Benchmark](docs/guides/custom-benchmark.md)
- [CI/CD Integration](docs/guides/ci-cd-integration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON, Markdown, HTML, CSV, and diff report files when used through its evaluation CLI.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

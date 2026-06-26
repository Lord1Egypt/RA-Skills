## Description: <br>
Benchmark Store helps initialize benchmark databases, compare skill scores against historical baselines, check Pareto-front regressions, and consult quality grading standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluation engineers use this skill to maintain local benchmark data, compare candidate skill results with frozen baselines, and identify Pareto-front regressions before release decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark databases and Pareto state can affect release decisions if corrupted or overwritten. <br>
Mitigation: Keep benchmark databases and Pareto state in a scoped directory, back them up before add/delete operations, and review comparison output before using it for gate decisions. <br>
Risk: Hidden-test files, passwords, and decrypted objects can expose sensitive evaluation materials. <br>
Mitigation: Protect hidden-test assets and passwords, and do not expose proposer-facing code to raw hidden-test objects. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/benchmark-store) <br>
- [Benchmark database](data/benchmark-database.md) <br>
- [Evaluation standards](data/evaluation-standards.md) <br>
- [Red-team guide](data/red-team-guide.md) <br>
- [Test cases](data/test-cases.yaml) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>
- [Prompt Injection Attacks](https://learnprompting.org/docs/prompt_hacking/introduction) <br>
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, SQLite, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite benchmark databases and Pareto state files when commands are run.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

The adjudication discipline and delivery gate for code security audits. Use when the user asks to audit the security of a piece of code, a pull request, a change, or to verify an existing vulnerability claim. It does three things: supply the deterministic facts a model cannot compute (callers, test coverage, git history origins), judge every claim against six gates, and downgrade any claim that cannot produce evidence to "observation" rather than a finding. The slash command may carry a mode word: pr = audit a change; graph = draw the provenance lineage of deleted code; repo = dependency surface only; claim = verify an existing vulnerability conclusion; gate = check an already-written report; help = print this table. With no mode word the full audit runs (the mapping table lives in the body). Not for: asking about the details of a single CVE, running an existing scanner once, pure documentation or formatting changes, or when the user explicitly wants a quick summary and accepts the risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modusensus](https://clawhub.ai/user/modusensus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to structure audits of repositories, code changes, and suspected vulnerabilities. It guides evidence-based conclusions and produces an audit report with claims that lack sufficient evidence marked as observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the audit workflow may involve running tests or exploit demonstrations from an untrusted project.

Mitigation: Get explicit approval for each command and run it in an isolated, disposable environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/modusensus/skills/euthyna-en)
- [Publisher profile](https://clawhub.ai/user/modusensus)
- [Bug classes](references/bug-classes.md)
- [Fact producers](references/fact-producers.md)
- [Fact contract](references/fact-contract.md)
- [Dependency audit](references/dependency-audit.md)
- [Change audit](references/change-audit.md)
- [Verification gates](references/verification-gates.md)
- [Meta mechanisms](references/meta-mechanisms.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Markdown]

**Output Format:** [Markdown audit reports with evidence citations and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode-specific audit guidance and findings; conclusions without sufficient evidence are downgraded to observations.]

## Skill Version(s):

0.11.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

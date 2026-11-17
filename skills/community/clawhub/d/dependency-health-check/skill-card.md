## Description:

Multi-ecosystem dependency audit to find outdated, vulnerable, unused, and license-incompatible packages across npm, pip, cargo, go, and composer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit dependency security, freshness, license compatibility, and unused packages across common package ecosystems. The skill guides an agent to produce a prioritized upgrade plan with risk assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to download, install, or run unpinned third-party audit tools in a project environment.

Mitigation: Run audits in a disposable container or virtual environment with pinned, preinstalled tools, and require approval before `npx`, `pip install`, or similar commands.

Risk: Automatic dependency fixes can change the environment or introduce breaking dependency updates.

Mitigation: Review proposed fixes before execution, avoid forceful automatic upgrades, and run the project's test suite after each upgrade batch.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized upgrade plan with dependency risk assessment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

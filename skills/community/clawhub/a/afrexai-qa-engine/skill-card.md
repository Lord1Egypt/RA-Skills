## Description: <br>
Complete quality assurance system for planning test strategy, writing tests, analyzing coverage, automating pipelines, performance and security testing, defect triage, and release readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to plan risk-based testing, generate test templates, review coverage, define CI quality gates, assess performance and security readiness, triage defects, and prepare releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested audit commands, CI quality gates, and release thresholds may be inappropriate for a specific project if applied without review. <br>
Mitigation: Review generated commands and thresholds against the project's stack, risk profile, and operational requirements before adding them to automation. <br>
Risk: Guidance to quarantine, delete, or rewrite flaky tests could remove useful coverage if the root cause is not understood. <br>
Mitigation: Require human review of test removals and keep issue links or replacement coverage for deleted or quarantined tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-qa-engine) <br>
- [Publisher profile](https://clawhub.ai/user/1kalin) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML templates, checklists, tables, and code or shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stack-agnostic QA methodology; outputs should be reviewed and adapted before applying commands, CI gates, deletions, or release decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

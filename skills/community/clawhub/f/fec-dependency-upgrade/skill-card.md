## Description: <br>
Helps agents plan, implement, and review frontend dependency upgrades, including lockfile changes, major framework migrations, CVE remediation, peer dependency conflicts, ESM/CJS shifts, build-tool compatibility, and CI verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute frontend dependency upgrades with source checks, batching strategy, risk classification, verification commands, rollback notes, and review guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency or lockfile changes may introduce build, type, test, or runtime regressions. <br>
Mitigation: Review proposed package and lockfile changes and run install, typecheck, test, build, and any relevant E2E, Storybook, or manual smoke checks before accepting changes. <br>
Risk: Major framework, build-tool, or test-tool migrations can miss breaking changes or compatibility boundaries. <br>
Mitigation: Use official release notes and migration guides, check peer dependencies and Node or browser support, and validate these migrations in separate batches. <br>
Risk: CVE-driven updates can over-upgrade runtime-critical packages when the exploitable path or fix impact is unclear. <br>
Mitigation: Assess the affected path and remediation impact first, then choose the smallest verified upgrade that resolves the relevant risk. <br>


## Reference(s): <br>
- [Dependency Upgrade Workflow](references/dependency-upgrade-workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-dependency-upgrade) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/bovinphang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, tables, and command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package upgrade lists, risk classifications, source references, verification commands, failure triage, and rollback recommendations.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata, package.json, metadata.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

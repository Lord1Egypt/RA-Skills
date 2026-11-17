## Description:

A HarmonyOS application development workflow that helps agents guide PRD creation, code generation, TDD, debugging, build validation, and release/version management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to standardize HarmonyOS app delivery from requirements through release, including scaffolding models, services, pages, and viewmodels, running TDD loops, diagnosing issues, and checking quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some scripts can install persistent Git hooks in the target repository.

Mitigation: Review existing hooks first and run hook installation only in repositories where replacing or adding hooks is acceptable.

Risk: The mock server can expose local endpoints and mock data.

Mitigation: Bind or firewall the server before use and avoid putting real personal or production data in mock files.

Risk: Mock server setup can install mutable npm dependencies.

Mitigation: Pin and review npm dependencies before running mock-server initialization or startup commands.

Risk: Generated files or update workflows can overwrite project files.

Mitigation: Run scripts in a clean version-controlled workspace and use simple trusted identifiers for generated file names.

Risk: Some advertised tooling may fail because lint.sh and visualize.sh failed shell syntax checks during inspection.

Mitigation: Verify these scripts manually before relying on their linting or visualization results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shixiangyu2/skills/app-dev-workflow)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Roadmap](artifact/ROADMAP.md)
- [Comparison](artifact/COMPARISON.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated project or code file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify project files when the user runs the bundled scripts; review paths and commands before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

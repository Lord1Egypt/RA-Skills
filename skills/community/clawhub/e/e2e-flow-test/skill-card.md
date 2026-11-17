## Description:

E2E automation engineer skill for Playwright-driven flow validation, browser interaction coverage, and end-to-end regression checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to validate multi-step UI flows, Playwright-backed browser behavior, and end-to-end regressions in Weline projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Weline-specific E2E commands and project documentation, so it may fail or validate the wrong path in unsupported repositories.

Mitigation: Use it only where `php bin/w e2e:run` and the referenced Weline project docs are available, and confirm the selected scenario matches the changed user flow.

Risk: Browser validation may require login data, seed data, or dedicated runtime state.

Mitigation: Review test credentials, seed data, ports, and runtime setup before execution, and clean up any dedicated runtime instance after validation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with command snippets and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports executed scenarios, pass or failure evidence, prerequisite setup, and residual gaps.]

## Skill Version(s):

1.1.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

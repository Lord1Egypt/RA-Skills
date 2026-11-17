## Description:

Write reliable E2E and component tests with Cypress avoiding flaky selectors, race conditions, and CI failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to set up Cypress and write or debug E2E, component, and API tests with reliable selectors, network intercepts, custom commands, and CI configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cypress Cloud recording can send test results outside the local project when enabled.

Mitigation: Remove or explicitly opt into Cypress Cloud recording, and avoid production secrets or sensitive data in tests.

Risk: CI screenshots, videos, and reports can retain sensitive application data.

Mitigation: Restrict CI artifact access and retention, especially for failure artifacts.

Risk: Optional cross-project memory can retain testing notes outside the repository.

Mitigation: Avoid creating ~/cypress/memory.md unless cross-project retention is intended.

Risk: Unpinned Cypress and CI action versions can drift over time.

Mitigation: Pin Cypress and GitHub Actions versions where possible.

## Reference(s):

- [ClawHub Cypress skill page](https://clawhub.ai/ivangdavila/skills/cypress)
- [Cypress skill homepage](https://clawic.com/skills/cypress)
- [Setup guidance](artifact/setup.md)
- [Selectors guide](artifact/selectors.md)
- [Custom commands guide](artifact/commands.md)
- [Network and API testing guide](artifact/network.md)
- [CI/CD configuration guide](artifact/ci.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with TypeScript, YAML, JSON, Dockerfile, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cypress test files, configuration updates, custom commands, CI workflow templates, and optional memory guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

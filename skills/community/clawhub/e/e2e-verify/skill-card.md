## Description:

Verifies web application changes in a real browser and routes each request to either an ephemeral smoke walk or a durable regression test, with safety gates for non-production targets and throwaway data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify web UI changes against localhost or staging, capture observed browser behavior, and decide when critical flows need durable end-to-end tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent browser-use helpers can source project .env files as shell code and overexpose LLM credentials.

Mitigation: Review before installing, avoid sourcing the generated activate.sh inside untrusted repositories unless project .env loading is removed, and prefer explicitly exported limited credentials.

Risk: Browser verification can expose sensitive application data or mutate real user state if pointed at production.

Mitigation: Use the skill only against localhost or staging with throwaway accounts and sanitized data.

Risk: Unpinned browser-use and Playwright dependencies can change behavior across installations.

Mitigation: Consider pinning dependencies and using local models for sensitive applications.

## Reference(s):

- [browser-use engine guidance](references/browser-use.md)
- [browser-use repository](https://github.com/browser-use/browser-use)
- [browser-use documentation](https://docs.browser-use.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with observations, code snippets, shell commands, and test or configuration files when durable checks are requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should enumerate walked paths, quoted observations, findings, and paths not walked.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

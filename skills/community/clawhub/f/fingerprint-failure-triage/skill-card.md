## Description:

Read a liarjs fingerprint report and attribute each failing check to the component that produced it: launch configuration, page-modifying layer, network path, machine image, or expected headless and datacenter behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liarjsdev](https://clawhub.ai/user/liarjsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to interpret low-scoring liarjs fingerprint reports, group failing checks by responsible component, and explain which findings are inherent to headless, proxied, datacenter, or image-based environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a third-party npm CLI through npx.

Mitigation: Pin an exact reviewed liarjs version, install with lockfile or integrity verification, and run scans in a low-privilege sandbox without unnecessary credentials.

Risk: Fingerprint scan scores can be misread as predictions of how real sites will treat a browser.

Mitigation: Use the skill's guidance to report only internal coherence findings and avoid outcome forecasts.

## Reference(s):

- [Interpreting a failing check](references/interpreting-checks.md)
- [liarjs CLI field notes](https://liarjs.dev/cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise findings and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups fingerprint failures by source and flags expected headless, proxy, datacenter, or image-related findings.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Analyzes frontend performance issues including LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency, then suggests prioritized practical optimizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to diagnose slow first paint, poor Core Web Vitals, runtime jank, and oversized bundles, then plan prioritized fixes with validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional bundle-analysis command may install or execute an unpinned package.

Mitigation: Use a project-local pinned analyzer from the lockfile, or run the command in a sandbox without sensitive credentials.

Risk: Performance recommendations can be misapplied when based only on subjective reports of slowness.

Mitigation: Collect Lighthouse, Performance recording, Network waterfall, or bundle-analysis data before selecting fixes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown performance report with prioritized recommendations, validation steps, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest project-local frontend measurement tools such as Lighthouse, Performance recordings, or bundle analyzers.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

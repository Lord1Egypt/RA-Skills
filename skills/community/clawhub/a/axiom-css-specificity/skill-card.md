## Description:

CSS specificity calculator that computes (a, b, c) specificity for CSS selectors, including :is(), :not(), :where(), combinators, and attribute selectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to debug CSS specificity conflicts, audit selectors for excessive specificity, and compare two selector rules during CSS maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server-resolved GitHub import provenance is unavailable for this version.

Mitigation: Use the server release metadata and artifact hashes for review, and require separate provenance confirmation when package origin matters.

Risk: The helper does not render CSS, resolve !important, support @scope, or support CSS preprocessor syntax.

Mitigation: Use browser or CSS tooling for cascade rendering and preprocessor-specific validation, and treat this skill as a specificity calculator only.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; the helper can emit JSON specificity breakdowns.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local Python helper using the standard library; no LLM, network use, persistence, or destructive behavior indicated by security evidence.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

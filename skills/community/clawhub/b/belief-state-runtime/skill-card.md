## Description:

LLM-driven epistemic reasoning engine. Evaluates claims against evidence, outputs calibrated confidence and structured belief state (VERIFIED/CONTESTED/UNCERTAIN). Use when the agent needs to assess whether information is trustworthy, detect contradictions in evidence, or quantify uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hqzzdsda](https://clawhub.ai/user/hqzzdsda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to assess whether a claim is supported, contested, or uncertain after gathering evidence. It is suited for reliability checks, contradiction detection, and confidence reporting where results remain advisory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User claims and evidence may be sent through the host agent's search or LLM workflows.

Mitigation: Avoid private, proprietary, personal, regulated, or unreleased claims unless that routing is acceptable and clearly authorized.

Risk: Adversarial evidence text or spoofed-looking source domains can influence the confidence score.

Mitigation: Review sources, corroborate important claims with trusted references, and treat outputs as advisory rather than determinative.

Risk: VERIFIED, CONTESTED, and UNCERTAIN labels can be overread as final truth judgments.

Mitigation: Present the confidence score, confidence range, and key limitations with the state label for consequential uses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hqzzdsda/skills/belief-state-runtime)
- [Project Homepage Listed By Skill](https://github.com/hqzzdsda/belief-state-runtime)
- [Belief State Runtime Configurator](https://hqzzdsda.github.io/belief-state-runtime/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON assessment results and concise explanatory Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces VERIFIED, CONTESTED, or UNCERTAIN state labels with confidence scores, confidence ranges, extracted feature booleans, and short summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

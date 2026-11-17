## Description:

Recommend optimal flow cytometry gating strategies for specific cell types and fluorophores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, cytometry operators, and developers use this skill to generate offline JSON recommendations for gating strategy, fluorophore channel and spillover considerations, panel optimization, compensation notes, and quality-control checks for selected cell types and fluorophores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated flow cytometry recommendations may be incorrect, incomplete, or unsuitable for clinical, regulatory, or protocol-critical decisions.

Mitigation: Treat outputs as experimental decision support and have qualified domain experts verify gating strategy, compensation, controls, and panel design before use.

Risk: The optional output path can overwrite an existing file selected by the user.

Mitigation: Use a noncritical destination path and review the target before running with --output.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [JSON to stdout or an optional JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic recommendation data from user-provided cell types, fluorophores, optional instrument name, and experiment purpose.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter differs: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

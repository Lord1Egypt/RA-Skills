## Description:

Solve and analyze steady incompressible fluid networks from TOML definitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w1965857192yf-dotcom](https://clawhub.ai/user/w1965857192yf-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define, validate, solve, and compare steady incompressible fluid network scenarios from TOML inputs. It supports pressure, flow, velocity, connectivity, and load-threshold reliability analysis for one scenario or all named scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-supplied output paths can overwrite or create files.

Mitigation: Write outputs to a dedicated project directory and review output paths before execution.

Risk: Caller-supplied TOML and Markdown template paths may read unintended local files.

Mitigation: Run the skill on project-specific inputs and avoid broad or sensitive filesystem paths.

Risk: Unpinned runtime dependencies can reduce reproducibility.

Mitigation: Pin scipy, networkx, and tomli versions in controlled deployments.

## Reference(s):

- [TOML Schema Reference](artifact/references/toml_schema.md)
- [ClawHub Skill Page](https://clawhub.ai/w1965857192yf-dotcom/skills/fluid-network-slover)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Plain text summaries, JSON result payloads, Markdown reports, and TOML templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write requested JSON, Markdown, or TOML files to caller-supplied paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

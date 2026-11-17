## Description:

GAIN predicts rice agronomic traits from genotype and environmental data using pre-trained MMoE deep learning models and supports climate-stress scenario analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianlvdouhua](https://clawhub.ai/user/qianlvdouhua)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agronomy analysts use GAIN to estimate rice traits from built-in or user-provided genotype data, location-specific environmental data, and optional climate-stress scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified PyTorch model files can execute code if model directories are replaced or come from untrusted sources.

Mitigation: Install and run the skill in an isolated, unprivileged Python environment and only use model files whose provenance and hashes have been verified.

Risk: Weather lookups may contact NASA POWER and write cached CSV files under the skill directory.

Mitigation: Review network and cache behavior before deployment, and restrict outbound access or pre-populate trusted weather data when external calls are not allowed.

## Reference(s):

- [GAIN ClawHub Skill Page](https://clawhub.ai/qianlvdouhua/skills/gain)
- [NASA POWER Daily Point API](https://power.larc.nasa.gov/api/temporal/daily/point)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON or table prediction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Predictions may include genotype-only, genotype-plus-environment, and stress-scenario values with trait metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

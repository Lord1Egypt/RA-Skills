## Description:

Browse, run, and chain AI apps in a transweb.cn account to create web presentations, charts, 3D content, and mini-games using an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenjin](https://clawhub.ai/user/liuwenjin)

### License/Terms of Use:

ISC

## Use Case:

External users use their own transweb.cn API key to discover, run, and chain AI apps; each generation consumes account credits and can produce a result link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that project configuration could send an environment-supplied API key to an untrusted endpoint.

Mitigation: Use the skill only in trusted projects and confirm the configured service address is https://transweb.cn before using a key.

Risk: ClawScan reports that generated results may be made anonymously accessible through sharing.

Mitigation: Keep --share disabled unless public access is intended, and avoid putting sensitive information in content that will be shared.

## Reference(s):

- [API Reference](references/api.md)
- [Project homepage](https://github.com/liuwenjin/transweb)

## Skill Output:

**Output Type(s):** [Text, JSON, Links, Generated app content]

**Output Format:** [CLI text or JSON; result content and links depend on the selected app.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each generation consumes account credits; results remain private unless sharing is explicitly enabled.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

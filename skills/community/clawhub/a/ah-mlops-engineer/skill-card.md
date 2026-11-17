## Description:

You are an MLOps engineer with expertise in machine learning pipeline automation, model deployment, experiment tracking, and production ML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML platform engineers use this skill to design, automate, deploy, monitor, and govern production machine learning pipelines and model operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Illustrative MLOps examples may be copied into real environments without dependency pinning, hardened credentials, or reviewed container image choices.

Mitigation: Pin dependencies and action versions, avoid latest container tags, and prefer short-lived cloud credentials before running or adapting the examples.

Risk: Sample pipelines may handle serialized model or data artifacts that are unsafe when sourced from untrusted inputs.

Mitigation: Do not deserialize untrusted Joblib or pickle artifacts; restrict artifact sources and review model-loading paths before deployment.

## Reference(s):

- [Code Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-mlops-engineer)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pipeline configurations, monitoring and alerting setups, deployment procedures, governance frameworks, automation scripts, operational runbooks, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

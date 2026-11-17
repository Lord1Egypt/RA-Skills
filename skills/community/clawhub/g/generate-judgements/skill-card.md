## Description:

Use when creating or updating test judgement definitions for an agent skill evaluation YAML config by analyzing a skill's SKILL.md and reference files to produce fine-grained yes/no judge questions with scope tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or update evaluation YAML for agent skills, especially the judge_definitions used by the mlflow-skills automated evaluation framework. It helps turn skill workflows, behavioral rules, and output requirements into scoped LLM judge questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated evaluation YAML may include incorrect judge definitions or environment fields if the reviewed skill is misunderstood.

Mitigation: Review the inferred scopes, judge definitions, and generated environment fields before approving any YAML write.

Risk: Committed YAML files can accidentally contain real API keys or other secrets.

Mitigation: Keep generated environment placeholders empty and use local environment variables or secret management for actual credentials.

## Reference(s):

- [Judgement Writing Patterns](artifact/references/judgement-patterns.md)
- [YAML Config Specification](artifact/references/yaml-config-spec.md)
- [mlflow-skills](https://github.com/panlm/mlflow-skills)
- [ClawHub Skill Page](https://clawhub.ai/panlm/skills/generate-judgements)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration]

**Output Format:** [Markdown discussion with YAML judge_definitions or updated evaluation YAML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for user confirmation before finalizing scopes and before writing or updating YAML.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

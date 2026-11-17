## Description:

生成标准化、模型可直接消费的自动化测试用例 JSON 套件，用于根据需求文档、原型图、页面说明、接口文档、用户故事、缺陷描述或自然语言需求产出可交给模型或自动化代理执行的测试用例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[deathknightorg](https://clawhub.ai/user/deathknightorg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to convert requirements, prototypes, API docs, user stories, bug reports, or natural-language requests into structured JSON test suites for Web UI, API, end-to-end, regression, smoke, and acceptance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Locale and timezone defaults may not match non-Chinese projects.

Mitigation: Review or override the default locale and timezone before using generated suites outside the intended project context.

Risk: Generated cases for production, payment, deletion, or irreversible actions could cause harmful effects if executed directly.

Mitigation: Keep those cases disabled unless explicitly authorized and require assumptions that call out the risk.

Risk: Incomplete source materials can lead to inferred selectors, endpoints, or assertions.

Mitigation: Record assumptions in the JSON suite and validate saved outputs with artifact/scripts/validate_test_suite_json.py before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deathknightorg/skills/generate-model-ready-test-cases-cn)
- [Model-ready test suite JSON schema](artifact/references/test-suite-schema.md)
- [Test case design playbook](artifact/references/test-design-playbook.md)

## Skill Output:

**Output Type(s):** [JSON, guidance, shell commands]

**Output Format:** [JSON code block by default, with optional concise Markdown or validation command when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured test suites with stable case IDs, step IDs, actions, assertions, placeholders, assumptions, defaults, and enabled flags.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

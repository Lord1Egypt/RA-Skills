## Description:

Generates a printable three-part static HTML exam review plan from knowledge_map.json, including a knowledge structure map, weak-point alerts, and a study plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoucha833-lang](https://clawhub.ai/user/zhoucha833-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Students and exam-preparation agents use this skill after an exam sprint analysis to turn a knowledge map into a static, printable review plan. It summarizes exam scope, weak areas, and phased study tasks, then asks whether to generate practice questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated HTML loads ECharts from bootcdn.net when opened.

Mitigation: Review network access requirements before deployment and prefer a version that bundles dependencies locally for restricted environments.

Risk: Study data from knowledge_map.json is embedded into the generated HTML.

Mitigation: Avoid including sensitive personal or exam-preparation data unless the output location and sharing path are controlled.

Risk: Unsafe HTML generation could allow unescaped knowledge-map content to affect the report page.

Mitigation: Escape or sanitize knowledge-map values before inserting them into HTML or JavaScript placeholders.

Risk: The skill can overwrite an HTML report for the same date when regenerating.

Mitigation: Confirm overwrite behavior is acceptable or add versioned output filenames before use.

Risk: The artifact contains authority-like execution language and silent-error behavior.

Mitigation: Require normal agent precedence rules, visible error reporting for blocking failures, and human review before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhoucha833-lang/skills/exam-mindmap-generator)
- [Design Specification](artifact/references/design-spec.md)
- [Review Plan Generation Rules](artifact/references/node-rules.md)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Static HTML file plus a short follow-up prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an exam-mindmap-YYYYMMDD.html review plan and may overwrite the previous file for the same date.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

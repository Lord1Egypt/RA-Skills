## Description:

7-agent paper review system on Hermes Agent. 6 modes (full/re-review/quick/methodology-focus/guided/calibration). 5-panel review with editorial decision, revision roadmap, and calibration metrics. Uses delegate_task for each reviewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

Researchers, authors, and editorial reviewers use this skill to assess academic manuscripts across methodology, evidence, argument quality, domain fit, and revision readiness. It can produce full peer-review panels, quick editorial assessments, re-review checks, guided improvement feedback, and calibration reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscript content and intermediate review outputs are processed through a delegated multi-agent workflow.

Mitigation: Use the skill only with manuscripts suitable for that workflow, and remove confidential or unnecessary material before review.

Risk: Included cross-model verification protocols can send manuscript content to external model APIs when enabled with user API keys.

Mitigation: Keep cross-model verification disabled for confidential, embargoed, proprietary, or personal-data-heavy papers unless the user explicitly approves the named provider.

Risk: The top-level file-only disclosure does not fully match referenced protocols that can use external API calls.

Mitigation: Review the configuration before use, rely on dedicated restricted API keys, and prefer a corrected release whose security disclosure matches its network behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/skills/academic-paper-reviewer)
- [Original Repository](https://github.com/Imbad0202/academic-research-skills)
- [Review Criteria Framework](references/review_criteria_framework.md)
- [Quality Rubrics](references/quality_rubrics.md)
- [Editorial Decision Standards](references/editorial_decision_standards.md)
- [Statistical Reporting Standards](references/statistical_reporting_standards.md)
- [Calibration Mode Protocol](references/calibration_mode_protocol.md)
- [Cross-Model Verification Protocol](shared/cross_model_verification.md)
- [Integration Guide](references/integration_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown review reports, editorial decisions, revision roadmaps, calibration reports, and configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are mode-dependent and may include reviewer panel findings, weighted editorial decisions, prioritized revision actions, and calibration metrics.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

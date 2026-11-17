## Description:

Provides an adversarial verification loop for cross-model distillation by testing distilled decision rules or student skills against adversarial cases and reporting robustness, overall quality, and rules that need rework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether distilled decision rules or student skills hold up against adversarial examples before deployment or retraining decisions. It returns rule-level robustness, an overall distillation quality score, and weak rules that need rework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification may execute Python code from the student skill directory being checked.

Mitigation: Run the skill in a sandbox or only against student skill directories that are already trusted and reviewed.

Risk: The learning module can retain cross-session notes, preferences, and usage history in learned_patterns.json.

Mitigation: Do not store secrets or sensitive notes through learner.py, and inspect or delete learned_patterns.json when retained history is not desired.

Risk: Robustness scores can be too high when adversarial cases do not cover important edge cases.

Mitigation: Use broad, representative adversarial cases and treat the score as a quality signal rather than proof that the distilled rule is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/distillation-adversarial-verify)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure standard-library Python; local execution; self-test sample available.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

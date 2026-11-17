## Description:

Axiomata Skill Evaluator Zh helps agents evaluate OpenClaw skill quality with bundled Axioma five-dimension scoring and ISO 25010 structural checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to run local, Chinese-language heuristic quality checks before release, during improvement work, or as part of skill audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluator's quality scores are heuristic and may overstate production readiness.

Mitigation: Treat reports as advisory and use manual review before relying on results for release decisions.

Risk: The --all mode can inspect every sibling skill directory rather than a single intended target.

Mitigation: Run the evaluator on an explicit skill path unless broad local auditing is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiomata-skill-evaluator-zh)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces heuristic quality scores, structural check summaries, and improvement recommendations.]

## Skill Version(s):

3.0.1 (source: release evidence; artifact body and script mention 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Live geopolitical intelligence analysis with 39 analytical modules and real-time data integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimaansari](https://clawhub.ai/user/nimaansari)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, policy teams, and researchers use this skill to structure geopolitical assessments, gather live public-source indicators, compare actor behavior, identify intelligence gaps, and produce scenario-oriented analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live public-source queries can send topics, country names, app names, and related parameters outside the local machine.

Mitigation: Run the skill only when network disclosure is acceptable, review query contents before execution, and avoid using sensitive operational details in live lookups.

Risk: Optional ACLED credentials may be handled by the included data-fetch script.

Mitigation: Use a virtual environment, prefer environment-based secret handling or protected local prompts, and avoid passing credentials on the command line or storing them in shared logs.

Risk: Sanctions-evasion and verification material can be dual-use or legally sensitive.

Mitigation: Treat those modules as analytical references, require human review, and apply legal, compliance, and policy guardrails before acting on outputs.

Risk: The server security summary says the skill misstates network use, credential requirements, and packaged files.

Mitigation: Validate packaged files and expected network behavior in a controlled environment before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nimaansari/skills/geopolitical-analyst-skill)
- [Publisher profile](https://clawhub.ai/user/nimaansari)
- [Sources reference](references/sources.md)
- [Early-warning reference](references/early-warning.md)
- [Scenario-modeling reference](references/scenario-modeling.md)
- [Verification-challenge reference](references/verification-challenge.md)
- [Sanctions-evasion reference](references/sanctions-evasion.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with optional JSON data-fetch results and shell or Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live public-source queries when data-fetch scripts are run; analytical outputs require human review for uncertainty, source quality, and legal or compliance context.]

## Skill Version(s):

0.1.2 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

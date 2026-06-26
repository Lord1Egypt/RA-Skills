## Description: <br>
Help AI understand a user's cognitive style, output preferences, and value orientation so it can generate deliverables that better match what they actually want. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lakendocean](https://clawhub.ai/user/Lakendocean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn questionnaire answers and messy preference descriptions into reusable agent-readable collaboration profiles. It helps produce stable AI_USER_PROFILE.md, USER.md, WORKSTYLE.md, or COLLAB_PROTOCOL.md files for future AI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated profiles can contain private workplace details or sensitive personal preferences if the user provides them. <br>
Mitigation: Review generated Markdown before saving, sharing, or reusing it with future agents, and omit sensitive details that should not persist. <br>
Risk: A partial or contradictory questionnaire session can produce an incomplete collaboration profile. <br>
Mitigation: Mark unresolved items in Known Unknowns and run a conflict-calibration round before treating the profile as stable. <br>


## Reference(s): <br>
- [questionnaire-v1.md](references/questionnaire-v1.md) <br>
- [inference-rules.md](references/inference-rules.md) <br>
- [output-schema.md](references/output-schema.md) <br>
- [templates.md](references/templates.md) <br>
- [examples.md](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown profile files with structured headings and concise prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a single AI_USER_PROFILE.md or split USER.md, WORKSTYLE.md, and COLLAB_PROTOCOL.md outputs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

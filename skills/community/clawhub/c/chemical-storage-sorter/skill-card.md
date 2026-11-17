## Description:

Sort chemicals by compatibility for safe laboratory storage. Prevents dangerous reactions by segregating incompatible chemicals (acids, bases, oxidizers, flammables) and provides storage recommendations compliant with safety regulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External lab personnel, EHS staff, and developers use this skill to classify chemical inventories into storage groups, flag incompatible pairs, and draft storage plans for qualified human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or incomplete chemical classification could lead to unsafe storage decisions.

Mitigation: Treat output as a rough draft and verify every classification and compatibility decision against current SDSs, institutional EHS procedures, and qualified human review.

Risk: Unknowns, mixtures, multi-hazard chemicals, toxics, cyanides, oxidizers, and compatibility decisions may exceed the skill's rules.

Mitigation: Do not use the skill as the final authority for those cases; segregate uncertain materials and escalate to qualified EHS review.

Risk: The security review notes broader agent permissions than the core sorting function needs.

Mitigation: Install and run with tight sandboxing and reduced permissions.

## Reference(s):

- [OSHA Chemical Storage Guidelines](https://www.osha.gov/chemical-storage)
- [SDS Search (MSDSOnline)](https://www.msdsonline.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline Python and bash examples; CLI output is plain text storage plans and compatibility warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are draft guidance and require current SDS, institutional EHS procedures, and qualified human review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

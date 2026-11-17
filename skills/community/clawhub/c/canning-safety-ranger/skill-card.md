## Description:

Use when canning or preserving food at home (or evaluating a canning recipe) — jars, acidity, pressure vs water-bath, altitude, storage, or suspect-jar triage. Screens recipes against botulism rules, computes process-time/pressure corrections, and triages spoiled vs safe jars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Home canners use the skill to screen a planned recipe or process, understand altitude and jar-size adjustments, and assess a suspect jar. Its verdicts and process guidance need review against the exact tested USDA/NCHFP process before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checks or process corrections could approve unsafe food or give incorrect preservation instructions.

Mitigation: Do not rely on this release for canning or eating decisions until corrected; follow the exact tested USDA/NCHFP process for the food, preparation, jars, equipment, and altitude.

Risk: Advice to boil suspect food before tasting or open suspect jars underwater conflicts with NCHFP handling and disposal guidance.

Mitigation: Do not use that suspect-jar advice; follow NCHFP handling and disposal guidance.

## Reference(s):

- [Tested-Process Tables — Water-Bath & Pressure](references/process-tables.md)
- [NCHFP: Identifying and Handling Spoiled Canned Food](https://nchfp.uga.edu/how/can/generalinformation/identifying-and-handling-spoiled-canned-food/)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/canning-safety-ranger)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text, Shell commands]

**Output Format:** [Text verdicts and safety guidance, with optional command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the food, preparation, jar size, method, equipment, and altitude; check the exact tested process.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

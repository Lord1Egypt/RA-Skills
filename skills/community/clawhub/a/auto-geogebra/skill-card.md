## Description:

Helps university mathematics teachers turn teaching ideas into runnable, editable, and verifiable GeoGebra dynamic demonstrations by clarifying requirements, designing interaction variables, generating GeoGebra commands, validating them, and exporting .ggb files when the local environment supports it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhjx19](https://clawhub.ai/user/zhjx19)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users, especially university mathematics teachers and instructional developers, use this skill to design classroom GeoGebra courseware for topics such as calculus, linear algebra, probability, statistics, and related mathematics courses. It produces requirement-confirmation notes, interaction-variable plans, validated GeoGebra command code, teacher-facing usage guidance, and optional .ggb exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional .ggb export can load GeoGebra's official browser engine from the network, which introduces supply-chain and reproducibility risk if the remote script changes.

Mitigation: Install only when comfortable with local Python/Node tooling; for sensitive material or strict reproducibility, pin and verify the package and use a reviewed local GeoGebra engine asset.

Risk: Generated demonstrations can pass static validation while still missing the intended teaching effect, especially for complex scripts, 3D objects, loci, or animation behavior.

Mitigation: Review the generated commands and run the resulting GeoGebra file before classroom use; treat validation summaries as correctness checks for low-level command issues, not as proof of pedagogical fit.

## Reference(s):

- [Skill page](https://clawhub.ai/zhjx19/skills/auto-geogebra)
- [GeoGebra manual](https://github.com/GeoGebra/manual)
- [Online GeoGebra batch executor fallback](https://ggbgen.pages.dev/)
- [Course routing reference](references/course-routing.md)
- [Command validation reference](references/command-validation.md)
- [Interaction patterns reference](references/interaction-patterns.md)
- [Teaching design patterns reference](references/patterns.md)
- [Common anti-patterns reference](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with GeoGebra command blocks, validation summaries, teacher-facing guidance, and optional .ggb files or preview assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local Python validation tools and optional Node/browser-based GeoGebra export tooling; no API keys are required.]

## Skill Version(s):

1.4.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

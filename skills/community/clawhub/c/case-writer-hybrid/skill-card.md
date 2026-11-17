## Description:

Expand a structured brief in `content-production/inbox/` into a reusable long-form markdown article draft, then run a local writer / critic / judge quality loop with a constrained humanization pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and publishing workflow developers use this skill to turn structured briefs into long-form article drafts with reusable writing packs and review traces. It is intended for a controlled local drafting loop that preserves supplied arguments and stops downstream handoff when quality gates fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated slug values from briefs can write generated files outside the documented draft folders.

Mitigation: Install only for trusted or pre-validated briefs, and validate slug/date fields plus output-path containment before processing third-party or automatically generated briefs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/case-writer-hybrid)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [Markdown article draft plus Markdown and JSON sidecar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit a quality-gate notice when the draft fails after up to 3 local review rounds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

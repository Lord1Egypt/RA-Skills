## Description:

Transforms short-term rental property details into Airbnb/VRBO listing copy, photo captions, house rules, guest FAQs, and automated guest message templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitflopez](https://clawhub.ai/user/gitflopez)

### License/Terms of Use:

MIT-0

## Use Case:

Short-term rental hosts, property managers, co-hosts, real estate investors, and hotel operators use this skill to create publication-ready listing and guest communication content for Airbnb, VRBO, and related booking platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompts request lock codes, WiFi passwords, unit access procedures, and emergency contact details that could expose sensitive property access information if entered into a general AI chat.

Mitigation: Use placeholders such as {{ACCESS_CODE}} and {{WIFI_PASSWORD}} in prompt runs, then substitute real values only inside a trusted booking or property-management platform.

Risk: Generated examples or drafts may contain live or reusable access details if a user entered real credentials while using the skill.

Mitigation: Review outputs before publishing or sending to guests, remove sensitive details from general-purpose AI transcripts, and rotate any real access codes or passwords that were entered into prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitflopez/skills/airbnb-str-listing-optimizer)
- [Publisher profile](https://clawhub.ai/user/gitflopez)
- [Artifact README](artifact/README.md)
- [Worked example](artifact/examples/las-vegas-strip-condo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown prompt outputs containing listing copy, photo captions, house rules, FAQ entries, and guest message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; users provide property, policy, access, WiFi, parking, checkout, and local recommendation details.]

## Skill Version(s):

1.0.0 (source: server evidence release.version, artifact/SKILL.md, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

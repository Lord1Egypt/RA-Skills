## Description:

Upload a photo to identify celebrities using Face8 Taiwan face recognition engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichendong](https://clawhub.ai/user/ichendong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit a local photo to Face8 for celebrity or public-figure recognition, with optional JSON output for downstream inspection. It can also register unknown faces or confirm suggested matches when the user intentionally chooses those commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photos and face data are sent to Face8 for recognition.

Mitigation: Use the skill only with images you are comfortable sending to Face8, and avoid submitting sensitive or unauthorized face images.

Risk: The --register and --confirm options can add or confirm faces in Face8's remote face database.

Mitigation: Use --register or --confirm only when you intentionally want to modify Face8 data; use the standard recognition command for lookup-only use.

Risk: Recognition results may be inaccurate.

Mitigation: Treat matches and confidence scores as suggestions and verify important identities through another trusted process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ichendong/skills/face8-celebrity)
- [Face8 FaceMaster](https://face8.ai/faceMaster/)
- [Face8 FaceMaster API](https://face8.ai/faceMaster/api)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text recognition summary or raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include celebrity names, confidence scores, face tokens, suggested matches, and registration or confirmation status.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

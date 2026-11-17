## Description:

Remove leftover speckle artifacts from transparent-background PNGs produced by matting or keying: semi-transparent haze remnants (alpha below threshold) and isolated island fragments (small connected alpha regions).

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to inspect and clean small haze remnants and isolated fragments in transparent PNGs produced by matting or keying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports gaps in file-protection safeguards around output paths and deletion.

Mitigation: Prefer a corrected release. If proceeding, run only the documented cleaner on copies in a fresh output folder and keep independent backups.

Risk: The included sharing helper can expose unrelated local files when used with untrusted HTML.

Mitigation: Avoid processing untrusted HTML with the sharing helper.

## Reference(s):

- [Alpha Despeckle on ClawHub](https://clawhub.ai/catsmansion/skills/alpha-despeckle)
- [Publisher profile: catsmansion](https://clawhub.ai/user/catsmansion)

## Skill Output:

**Output Type(s):** [PNG files, Text reports, Shell commands]

**Output Format:** [PNG images and plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; --apply writes changes and the documented workflow creates a backup.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

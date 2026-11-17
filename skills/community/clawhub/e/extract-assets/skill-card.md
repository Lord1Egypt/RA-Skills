## Description:

Find images, SVGs, videos, audio, and Lottie animations on a website and return their URLs or usable SVG markup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soraiabarroso](https://clawhub.ai/user/soraiabarroso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to locate website media for reference, analysis, or reuse where rights permit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted page URLs are sent to MiroMiro's external API.

Mitigation: Avoid submitting private or sensitive URLs without authorization.

Risk: Requests consume credits; render mode loads the target page in a remote browser for additional credits.

Mitigation: Confirm the need and credit cost before retrying with render mode.

Risk: Website logos, photos, audio, and video may carry reuse restrictions.

Mitigation: Check rights before republishing or redistributing extracted assets.

## Reference(s):

- [MiroMiro API documentation](https://miromiro.app/api/docs)

## Skill Output:

**Output Type(s):** [Text, Code]

**Output Format:** [Markdown with asset URLs and, when requested, inline SVG markup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be capped or truncated; JavaScript-rendered media may require a render-mode retry.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

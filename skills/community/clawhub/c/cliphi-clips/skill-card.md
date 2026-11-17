## Description:

Turns the user's long videos into ready-to-post vertical clips with captions and branding, using the Cliphi API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cliphi](https://clawhub.ai/user/cliphi)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and creators use this skill to find strong moments in long videos, review free preview links, and render selected short-form clips with captions and branding through Cliphi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Cliphi API key and sends user-provided video URLs to Cliphi for processing.

Mitigation: Install only when that data sharing is acceptable, keep the API key scoped to the user's Cliphi account, and revoke the key when access is no longer wanted.

Risk: Submitting jobs or rendering selected clips can spend Cliphi credits.

Mitigation: Show free previews first, state render costs from the API response, and require explicit user confirmation before any billed render.

Risk: Generated clips could be made from content the user does not have rights to use.

Mitigation: Use the skill only with videos the user owns or is authorized to repurpose, and keep a human in the loop before public posting.

## Reference(s):

- [Cliphi API reference](https://www.cliphi.com/cliphi-actions.json)
- [Cliphi API key settings](https://www.cliphi.com/studio/settings/api-keys)
- [Cliphi demo endpoint](https://www.cliphi.com/api/v1/demo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands, API response summaries, preview links, render confirmations, and clip URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLIPHI_API_KEY for authenticated Cliphi API calls; demo output is available without a key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

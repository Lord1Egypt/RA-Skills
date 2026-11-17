## Description:

Download the user's own Instagram Saved posts (images, and MP4 when asked) with Ego Lite cookies via ego-browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Instagram users use the skill to archive posts saved on their own account through an Ego Lite session, saving images by default and videos when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded media and the manifest may contain private information from the signed-in account.

Mitigation: Use the intended Instagram account and a dedicated output folder; keep exported files out of public repositories.

Risk: An optional Chrome-profile import can expose account data to the Ego session.

Mitigation: Review the profile import before using it and confirm the intended account is open in Ego.

Risk: The skill relies on the separately installed ego-browser, which was outside this security review.

Mitigation: Use an ego-browser installation you trust.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryso/skills/ego-instagram-saved-download)
- [Login guidance](references/login.md)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Downloaded image or MP4 files, a JSON manifest, and a JSON run summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are saved by default; videos or both can be requested. The post count is capped at 100.]

## Skill Version(s):

0.2.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

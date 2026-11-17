## Description:

Turn a confirmed new-drop script and authorized stills into one drop talking clip per still. This product drop video studio writes a speakable launch talking clip and new-drop announcement for each photo, then animates a 2 to 15s talking teaser. Use it for creator drop videos and talking teasers that stay one photo, one clip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and listing teams use this skill to turn confirmed product-drop details and authorized still images into a set of short talking announcement clips, with one clip per still.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Beatra authorization requests broader image- and music-generation permissions than this workflow needs.

Mitigation: Review the full authorization before connecting and request narrower permissions where possible; revoke device access in the Beatra Console if needed.

Risk: Selected media leaves the user's computer, and installation analytics have no documented opt-out.

Mitigation: Use only stills authorized for upload and review the service's data handling before connecting.

Risk: An uninstall flaw and corrupted shared inventory could disconnect other Beatra skills.

Mitigation: Review uninstall handling before removal and seek corrected uninstall behavior; check other Beatra skill connections if shared inventory is affected.

Risk: Voice cloning, speech synthesis, and video generation are separate paid stages.

Mitigation: Review and approve each stage's current price and scope before allowing its paid operation.

## Reference(s):

- [Beatra Creator Drop Talking skill page](https://beatra.ai/skills/creator-drop-talking)
- [Workflow](references/workflow.md)
- [Installation and authorization](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Video]

**Output Format:** [Labeled clip plan and spoken drop scripts, followed by separate talking teaser video clips]

**Output Parameters:** [2–8 clips per pack; each clip is 2–15 seconds and corresponds to one still]

**Other Properties Related to Output:** [Clips are delivered separately and are not stitched together.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

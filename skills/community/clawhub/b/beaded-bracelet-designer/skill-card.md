## Description:

Creates beaded-bracelet and other jewelry design drafts, hand-drawn sheets, and interactive 3D previews from prompts and reference images through a hosted jewelry-design service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Jewelry designers and makers use this skill to turn design ideas and reference images into bracelet concepts, multiview sketches, and online 3D previews. It also supports other jewelry types, including rings and necklaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image URLs are sent to a hosted jewelry-design service.

Mitigation: Submit only designs and image URLs you are comfortable sharing with that service.

Risk: The gateway access key grants access to the hosted API.

Mitigation: Keep the DEEPNLP_ONEKEY_ROUTER_ACCESS key private and avoid including it in prompts or shared outputs.

Risk: Returned workspace links may be accessible to anyone holding the link.

Mitigation: Share design workspace URLs only with intended recipients.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ai-hub-admin/skills/beaded-bracelet-designer)
- [Craftsman Beaded Bracelet Designer](https://craftsman-agent.aiagenta2z.com/app/jewelry-designer/beaded-bracelet)
- [OneKey access key setup](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Guidance, Links to design assets]

**Output Format:** [Markdown with links to hosted design sheets and interactive previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted API responses can include image URLs, a design blueprint, and a shareable workspace URL.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

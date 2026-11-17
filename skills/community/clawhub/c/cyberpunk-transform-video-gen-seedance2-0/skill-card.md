## Description:

Re-skin any everyday clip concept into neon-drenched, high-tech, augmented urban futures using WeryAI Seedance 2.0 only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text briefs or public HTTPS image inputs into short cyberpunk-style videos through WeryAI Seedance 2.0. It guides prompt expansion, parameter confirmation, CLI execution, and returning playable video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make paid WeryAI network calls using WERYAI_API_KEY.

Mitigation: Use a limited or separate WeryAI account where possible and require confirmation before each submission.

Risk: The helper script can submit broader video-generation requests than the Seedance-only workflow describes.

Mitigation: Before execution, verify the final JSON uses model SEEDANCE_2_0, allowed duration, resolution, and aspect ratio values, no negative_prompt, and only the intended HTTPS image input.

Risk: Runtime credentials are required for generation and status checks.

Mitigation: Keep WERYAI_API_KEY out of committed files and run the skill in a short-lived or isolated environment for higher assurance.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/cyberpunk-transform-video-gen-seedance2-0)
- [WeryAI video tasks API host](https://api.weryai.com)
- [WeryAI models registry API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with confirmation tables, inline shell commands, and playable video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WERYAI_API_KEY, Node.js 18+, public HTTPS image inputs, and JSON parameters constrained to SEEDANCE_2_0.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Transforms text briefs or public HTTPS image URLs into pastel fairytale-style short videos using WeryAI Seedance 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill through an agent to expand a short brief or public image URL into a confirmed WeryAI Seedance 2.0 video generation request and receive playable video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid WeryAI API key and sends prompts plus any referenced public image URLs to WeryAI.

Mitigation: Review prompts and image URLs for private or confidential content, confirm the expected credit cost, and only run with a WERYAI_API_KEY you are comfortable using.

Risk: The artifact documentation says the CLI does not enforce the package's SEEDANCE_2_0 model rule in code.

Mitigation: Before generation, verify the confirmation table and JSON payload set model to SEEDANCE_2_0.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/fairytale-dream-transform-video-gen-seedance2-0)
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI models registry host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline video links and JSON-backed CLI/API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY; paid WeryAI requests may send prompts and public image URLs to WeryAI.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

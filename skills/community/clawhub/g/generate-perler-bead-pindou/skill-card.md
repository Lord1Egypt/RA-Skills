## Description:

Generate 2D pixelized Perler Beads and Pindou patterns from a text prompt and reference image URLs, returning bead color codes and a workspace URL for instruction images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate Perler Bead or Pindou pattern data from text prompts and image URLs, including palette codes, grid cells, bead counts, and a shareable workspace for editing or exporting the design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and an optional OneKey access key may be sent to documented external services.

Mitigation: Review inputs before use, avoid sensitive prompts or private image URLs, and provide only the service-specific access key required for the request.

Risk: The execution path relies on credential-bearing outbound requests.

Mitigation: Use scoped credentials, keep the access key in the documented environment variable, and rotate or revoke the key if it is exposed.

Risk: The documented CLI path includes an unpinned external npx command.

Mitigation: Prefer direct, pinned, reviewed API calls or the included scripts, and pin any external CLI package before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/generate-perler-bead-pindou)
- [Publisher Profile](https://clawhub.ai/user/ai-hub-admin)
- [Craftsman Perler Bead App](https://craftsman-agent.aiagenta2z.com/app/pindou_perler_bead)
- [Craftsman Gallery](https://craftsman-agent.aiagenta2z.com/gallery)
- [Generate Perler Bead Pindou API Endpoint](https://craftsman-agent.aiagenta2z.com/craftsman-agent/api/v1/generate_perler_bead_pindou)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Guidance]

**Output Format:** [JSON API responses and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a color palette, bead grid, statistics, blueprint settings, generated image URL, session identifiers, and a shareable workspace URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

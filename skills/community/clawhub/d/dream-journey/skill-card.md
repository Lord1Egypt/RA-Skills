## Description:

Dream Journey turns recurring or vague dream scenes into travel planning by reconstructing the dream, matching real destinations with FlyAI search, planning itineraries, and producing post-trip reports and video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catshcrozhang](https://clawhub.ai/user/catshcrozhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to turn non-distressing dream imagery into destination suggestions, itinerary plans, booking links, photo-based trip reflections, HTML reports, and short-form video scripts. The skill includes a safety posture for frightening or traumatic dream descriptions and redirects those cases away from destination matching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run third-party CLI tooling and optional Node.js scripts.

Mitigation: Review install commands before use, avoid pipe-to-shell and sudo npm patterns, and pin or verify third-party CLI versions where possible.

Risk: Generated HTML reports may include untrusted dream text, itinerary data, or image URLs.

Mitigation: Treat generated HTML as untrusted content, review inputs before opening or sharing reports, and avoid embedding sensitive personal details.

Risk: Travel planning can lead users toward booking-related actions or commercial links.

Mitigation: Require explicit user confirmation before any booking-related step and disclose or omit commercial links when users request neutral planning.

Risk: Dream descriptions may include frightening, violent, or trauma-related content.

Mitigation: Use the skill's safety posture for distressing dream content and avoid matching those descriptions to real destinations.

## Reference(s):

- [Dream Journey ClawHub Skill Page](https://clawhub.ai/catshcrozhang/skills/dream-journey)
- [Detailed Reference](references/README.md)
- [Installation Guide](references/INSTALL.md)
- [Photo Report Guide](references/HOW-TO-ADD-PHOTOS.md)
- [FlyAI Open Platform](https://flyai.open.fliggy.com)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with inline shell commands, plus optional generated HTML and JSON files from local Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FlyAI CLI for real-time travel search and booking links; optional Node.js helpers generate local reports, prompts, quotes, and video-script previews.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

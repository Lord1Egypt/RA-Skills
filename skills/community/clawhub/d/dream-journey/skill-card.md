## Description: <br>
This skill turns recurring or unclear dream scenes into real travel destination matches, itineraries, visual prompts, trip verification, and post-trip reports using FlyAI travel search and local helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catshcrozhang](https://clawhub.ai/user/catshcrozhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to transform dream descriptions into destination recommendations, real-time travel options, itinerary guidance, booking links, and reflective trip artifacts. Developers can also use the included Node.js helpers to generate visual prompts, HTML reports, quotes, and short-video scripts from structured trip data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines travel search, booking-link flows, and possible account authorization through FlyAI or Fliggy. <br>
Mitigation: Install only if comfortable with those third-party services, require an itemized user confirmation before any booking or payment step, and complete payments only on the official Fliggy platform. <br>
Risk: Installation guidance includes command-line tooling and references a sudo curl-to-bash NodeSource setup path. <br>
Mitigation: Prefer trusted package-manager or official installer paths, and independently verify any privileged install command before running it. <br>
Risk: Generated HTML reports and photo workflows may include user travel details, personal photos, or other sensitive content. <br>
Mitigation: Use local or trusted photos where possible, avoid placing sensitive personal details in generated reports, and review generated HTML before sharing or opening it in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/catshcrozhang/dream-journey) <br>
- [Skill Reference Guide](artifact/references/README.md) <br>
- [Installation Guide](artifact/references/INSTALL.md) <br>
- [Photo Report Guide](artifact/references/HOW-TO-ADD-PHOTOS.md) <br>
- [Node.js](https://nodejs.org/) <br>
- [FlyAI Open Platform](https://flyai.open.fliggy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, HTML files] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper scripts can produce HTML reports, HTML previews, and text or JSON-derived content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Feizhu booking links, destination similarity scores, local report files, image-generation prompts, video scripts, and trip confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

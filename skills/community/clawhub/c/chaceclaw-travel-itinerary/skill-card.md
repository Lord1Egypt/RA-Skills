## Description: <br>
Generates travel itineraries from destination, duration, budget, traveler type, interests, and travel style, including daily plans, budget estimates, transportation suggestions, practical tips, and optional trip-management artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn basic trip preferences into structured itinerary guidance for leisure travel, including family, couples, solo, and group travel scenarios. It is most useful for drafting plans that must be checked against current official travel, weather, booking, safety, and budget sources before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate live weather, visa, booking, emergency, budget, or child-safety accuracy. <br>
Mitigation: Verify all time-sensitive and safety-critical details through official or current sources before relying on the itinerary. <br>
Risk: Trip plans, family details, expenses, and future travel information may be stored locally under the user's home directory. <br>
Mitigation: Avoid entering sensitive travel, finance, or family details unless local persistence is acceptable, and review or delete saved files after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ling-qian/chaceclaw-travel-itinerary) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown and plain text itinerary guidance, with optional JSON and text files for saved itineraries, expense tracking, diary templates, and PDF-style content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write trip, diary, photo-organization, and expense artifacts under the user's ~/.travel-planner directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

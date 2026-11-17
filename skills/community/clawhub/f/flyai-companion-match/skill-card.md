## Description:

带谁去哪 recommends companion-suitable attractions and travel plans by matching destination POI data with traveler profiles such as children, older adults, friends, or couples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agent operators use this skill to collect destination, companion, duration, accessibility, and preference details, then generate attraction recommendations and day-by-day plans suited to the whole group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global CLI installation and automatic @latest upgrades can change system state or install unexpected versions.

Mitigation: Review install commands before execution, avoid sudo unless explicitly approved, and prefer a pinned FlyAI CLI version when operational stability matters.

Risk: TLS certificate verification bypass can weaken network security.

Mitigation: Do not set NODE_TLS_REJECT_UNAUTHORIZED=0; resolve certificate failures through normal trust-store or network configuration fixes.

Risk: The skill may store family composition, location, budget, and travel preference details in memory or ~/.flyai/user-profile.md.

Mitigation: Save profile data only after explicit user consent, keep stored details minimal, and review or delete the profile when reuse is no longer desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-companion-match)
- [POI / Attraction Search](reference/search-poi.md)
- [Hotel Search](reference/search-hotel.md)
- [User Profile Storage](reference/user-profile-storage.md)
- [ask_user_question Tool](reference/tools.md)
- [Usage Examples](reference/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel recommendations with structured companion fit scores, itinerary suggestions, and optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions and use FlyAI search results to tailor recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

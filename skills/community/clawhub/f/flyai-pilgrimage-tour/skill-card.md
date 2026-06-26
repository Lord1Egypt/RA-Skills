## Description: <br>
Plans film, TV, variety-show, and anime location pilgrimages by finding real POIs, assembling itineraries, and adding flight, hotel, attraction, and booking guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to turn a movie, show, anime, or variety-program reference into a visitable location itinerary with POI checks, transportation, lodging, cost estimates, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install or upgrade a global, unpinned FlyAI CLI package. <br>
Mitigation: Review the package source and run the skill in an isolated environment before installing the CLI globally. <br>
Risk: The skill suggests commands that disable HTTPS certificate validation for travel and booking searches. <br>
Mitigation: Do not run commands with NODE_TLS_REJECT_UNAUTHORIZED=0; fix certificate trust issues and keep normal HTTPS validation enabled. <br>
Risk: The skill can save travel profile details that may include sensitive family, accessibility, or home-location information. <br>
Mitigation: Ask before saving profile data and avoid storing sensitive details unless the user intentionally requests persistence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-pilgrimage-tour) <br>
- [Skill instructions](SKILL.md) <br>
- [AI Search reference](reference/ai-search.md) <br>
- [Keyword Search reference](reference/keyword-search.md) <br>
- [POI / Attraction Search reference](reference/search-poi.md) <br>
- [Flight Search reference](reference/search-flight.md) <br>
- [Hotel Search reference](reference/search-hotel.md) <br>
- [Train Search reference](reference/search-train.md) <br>
- [Marriott Hotel Search reference](reference/search-marriott-hotel.md) <br>
- [Marriott Package Search reference](reference/search-marriott-package.md) <br>
- [User profile storage reference](reference/user-profile-storage.md) <br>
- [Example conversation](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with itinerary sections, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include travel profile read/write guidance and FlyAI CLI command examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Helps users choose a travel destination by collecting trip needs, excluding places they have already visited, and producing one personalized recommendation with rationale, itinerary, traveler-sourced perspective, and FlyAI links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walkingzq](https://clawhub.ai/user/walkingzq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users and travel-planning agents use this skill to collect trip constraints through conversation, compare candidate destinations internally, and present one best-fit destination with supporting rationale, itinerary guidance, real traveler perspective, and FlyAI-sourced links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run local shell setup commands and may install a global npm tool. <br>
Mitigation: Install and configure FlyAI through the user or platform in advance; do not allow automatic global npm installation or shell profile sourcing without approval. <br>
Risk: Destination searches and travel preferences may be sent to Xiaohongshu and FlyAI/Fliggy-style services. <br>
Mitigation: Avoid sending sensitive personal data to external travel services and use a fallback response when the user or platform does not allow those lookups. <br>
Risk: Real-time destination links or travel data may be unavailable. <br>
Mitigation: When FlyAI fails, fall back to no-link output rather than fabricating booking, POI, or destination links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/walkingzq/destination-finder) <br>
- [FlyAI integration guide](references/flyai-integration.md) <br>
- [Questionnaire guide](references/questionnaire-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown travel recommendation with structured sections, plain-text links, and FlyAI lookup commands used by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends one destination per request; uses real-time FlyAI data when available and falls back to no-link output when unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter metadata.version is 0.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

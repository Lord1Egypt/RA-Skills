## Description: <br>
AI wardrobe management for clothing inventory, AI outfit recommendations, fashion knowledge search, and virtual try-on. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houdamiao](https://clawhub.ai/user/houdamiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to call the AI Closet API for wardrobe management, outfit and OOTD workflows, AI recommendations, clothing knowledge search, and virtual try-on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send wardrobe data, personal images, and outfit history to the AI Closet service. <br>
Mitigation: Install only if the user trusts the service with that data, review uploads and record-creation actions before execution, and avoid sensitive or private image URLs. <br>
Risk: API keys passed in query strings may be exposed through logs, browser history, or shared URLs. <br>
Mitigation: Prefer the x-api-key header documented by the skill instead of query-string API keys. <br>
Risk: Uploaded photos and generated try-on assets may be retained or processed outside the local agent environment. <br>
Mitigation: Check the provider's retention and deletion policies outside the skill docs before using personal images. <br>


## Reference(s): <br>
- [Aicloset Skill on ClawHub](https://clawhub.ai/houdamiao/aicloset) <br>
- [Wardrobe and Product API](api-wardrobe.md) <br>
- [Outfit and OOTD API](api-outfit.md) <br>
- [AI Capabilities API](api-ai.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AICLOSET_API_KEY and curl; API calls exchange JSON or form data with the AI Closet service.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

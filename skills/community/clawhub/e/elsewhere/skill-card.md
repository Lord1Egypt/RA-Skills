## Description: <br>
A cross-space digital travel companion that creates a virtual character who travels to real destinations and sends postcard-like updates with AI-generated images aligned to real-world time, weather, and geography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamarc77](https://clawhub.ai/user/dreamarc77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create a personalized digital travel companion, plan and confirm trips, and receive postcard-style text and image updates during an automated simulated journey. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Gemini API key and sends travel context, persona details, and reference-image-derived prompts to Gemini. <br>
Mitigation: Install and run it only in a controlled environment, protect GEMINI_API_KEY, and review what user context and images are provided before execution. <br>
Risk: The scheduled update loop runs repeatedly during a trip and requires user control. <br>
Mitigation: Monitor the loop while active and stop it manually when the trip is complete. <br>
Risk: The skill stores persona, itinerary, and generated image files locally. <br>
Mitigation: Use only intended reference images and manage the local data/ and assets/generated/ directories according to the user's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/dreamarc77/elsewhere) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Generated images, Shell commands, Configuration] <br>
**Output Format:** [Markdown messages, JSON state files, shell commands, and PNG image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY; writes local runtime data under data/ and generated images under assets/generated/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

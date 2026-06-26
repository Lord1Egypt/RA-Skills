## Description: <br>
Drip Director is a deterministic streetwear and fashion image-production controller that captures user intent, enforces constraints, generates images with Nano Banana Pro, and routes critique through a separate Gemini call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoneislandartur](https://clawhub.ai/user/stoneislandartur) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and image-production agents use this skill to turn fashion or streetwear image requests into a confirmed, constraint-driven generation workflow with critique, regeneration, and convergence steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference images, generated outputs, briefs, and constraints may be sent to Google/Gemini services during critique or generation support. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid placing unrelated sensitive images in the inbound media folder. <br>
Risk: The workflow requires a Google API key and direct external API calls. <br>
Mitigation: Provide the API key through the expected environment variable and review command steps before execution. <br>
Risk: Intermediate generated images can be deleted during convergence cleanup. <br>
Mitigation: Preserve any intermediate outputs you want to keep before accepting the final convergence step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stoneislandartur/drip-director) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command blocks and structured state text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit user confirmations between stages and may produce local image-generation command outputs through the agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

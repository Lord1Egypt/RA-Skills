## Description: <br>
Automates Gemini website workflows for text Q&A and image generation, routing user prompts to the appropriate flow and returning answers or generated images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WJZ-P](https://clawhub.ai/user/WJZ-P) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask Gemini questions or request image generation through a signed-in Gemini web session, with task routing based on user intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent through the user's logged-in Gemini web session. <br>
Mitigation: Avoid sending secrets or sensitive personal, business, or account data unless sharing it with Gemini is acceptable. <br>
Risk: Generated images may temporarily exist as local downloads before being returned. <br>
Mitigation: Review local download handling and delete temporary files when retention is not needed. <br>
Risk: Website automation can fail or select a fallback model when Gemini UI elements or model availability change. <br>
Mitigation: Confirm the returned answer or image and retry with a shorter prompt or available model when automation reports a fallback. <br>


## Reference(s): <br>
- [Gemini Skill on ClawHub](https://clawhub.ai/WJZ-P/gemini-skill) <br>
- [Gemini Web App](https://gemini.google.com) <br>
- [Gemini Flow](references/gemini-flow.md) <br>
- [Intent Routing](references/intent-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, image files, guidance] <br>
**Output Format:** [Text or Markdown responses, with generated images returned as downloaded files when image generation succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's signed-in Gemini web session and may temporarily download generated images locally before returning them.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generate and edit images with Gemini API using pure Python stdlib. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cluka-399](https://clawhub.ai/user/Cluka-399) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate new images or edit existing images through Google's Gemini image API in environments where installing Python dependencies is undesirable or unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected input images, and related request data are sent to Google's Gemini API under the user's API key. <br>
Mitigation: Use an API key intended for this purpose, avoid sending sensitive images or prompts unless permitted, and monitor quota or billing. <br>
Risk: Generated output is written to the user-specified local path. <br>
Mitigation: Choose output paths carefully and avoid paths that could overwrite important files. <br>


## Reference(s): <br>
- [Google AI Studio API Key](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Image files saved locally, with Markdown and bash usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and can use an optional input image for editing.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

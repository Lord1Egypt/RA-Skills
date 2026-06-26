## Description: <br>
Generate ai blog image generator images with AI via the Neta AI image generation API (free trial at neta.art/open). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate blog hero or article images from text prompts through the Neta/TalesofAI image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the API token are sent to an external TalesofAI endpoint. <br>
Mitigation: Use the skill only with trusted content, avoid secrets or sensitive drafts in prompts, and use a dedicated or limited token where possible. <br>
Risk: Passing the token with a CLI flag can expose it in process listings or logs on shared systems. <br>
Mitigation: Avoid shared hosts for execution and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barbaraledbettergq/blog-image-claw-skill) <br>
- [Neta AI API token and trial](https://www.neta.art/open/) <br>
- [TalesofAI image API](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime scripts print an image URL or JSON result.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta/TalesofAI API token and sends prompts to api.talesofai.com.] <br>

## Skill Version(s): <br>
2.0.1 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

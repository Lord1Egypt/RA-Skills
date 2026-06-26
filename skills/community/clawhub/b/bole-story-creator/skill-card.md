## Description: <br>
Bole Story Creator calls the Bole AI platform to generate short drama stories, storyboards, and video production results from a user prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajianrong](https://clawhub.ai/user/jiajianrong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and agents use this skill to turn a story prompt into a short drama story, storyboard, and video-generation result through the Bole AI platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user prompts and generated project data to the Bole AI platform. <br>
Mitigation: Avoid confidential or regulated prompts and disclose the external Bole data transmission before use. <br>
Risk: The security review reports that the skill exposes a live bearer token in logs. <br>
Mitigation: Use only a revocable, least-privilege Bole access key and prefer a patched version that removes token logging. <br>
Risk: Video generation can take several minutes and relies on repeated network polling. <br>
Mitigation: Run it with bounded execution time, monitoring, and retry or cancellation handling appropriate for the agent environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [JSON object containing either result text with project details and a video link, or an error message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOLE_ACCESS_KEY and network access to the Bole AI platform; generation may take several minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

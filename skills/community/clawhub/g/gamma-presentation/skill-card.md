## Description: <br>
Generate professional presentations with Gamma AI. Just describe what you want - topic, outline, or full content - and get a polished deck. No Gamma account needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to turn a topic, outline, or content brief into a Gamma-generated presentation and retrieve a PDF, PPTX, or Gamma URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation prompts, outlines, and slide content are sent to Gamma for processing. <br>
Mitigation: Use only content approved for Gamma processing and avoid confidential or regulated data unless Gamma use is approved for that data. <br>
Risk: The skill can use local Gamma credentials from GAMMA_API_KEY or ~/.gamma/config.json. <br>
Mitigation: Use a scoped Gamma API key, review local Gamma configuration before running the skill, and avoid exposing the key in prompts or logs. <br>
Risk: The requested output path controls where generated PDF or PPTX files are written, and overwrite behavior is not documented. <br>
Mitigation: Choose explicit output paths in a reviewed directory and check generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [Gamma Presentation Generator on ClawHub](https://clawhub.ai/lmanchu/gamma-presentation) <br>
- [Gamma](https://gamma.app) <br>
- [Gamma Public API](https://public-api.gamma.app/v1.0) <br>
- [Bun Runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated presentation files as PDF or PPTX and JSON status from the script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bun and a Gamma API key. The script calls Gamma, polls for completion, and writes the requested output path when export succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

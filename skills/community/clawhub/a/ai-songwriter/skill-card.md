## Description: <br>
AI Songwriter turns a user-provided theme into Chinese pop lyrics, formats them for Suno, and automatically calls KIE/Suno to return generated song links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-hou-pe](https://clawhub.ai/user/jason-hou-pe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn a song theme into polished Chinese lyrics, Suno style tags, and generated song preview links without intermediate review prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends generated song content to KIE/Suno using a local API key and may consume provider credits without a review step. <br>
Mitigation: Use a scoped or low-risk API key where supported, review expected cost before execution, and run only when automatic external generation is acceptable. <br>
Risk: The helper script includes a hard-coded callback URL and additional cover or extend modes that are not fully described in the user-facing skill workflow. <br>
Mitigation: Review the helper script before deployment and restrict use to the documented generate path unless the extra modes and callback behavior have been approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-hou-pe/ai-songwriter) <br>
- [Publisher profile](https://clawhub.ai/user/jason-hou-pe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with generated lyrics, extracted hook text, and audio preview URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses KIE_API_KEY or SUNO_API_KEY and may execute a Node.js helper that polls KIE/Suno until generation completes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

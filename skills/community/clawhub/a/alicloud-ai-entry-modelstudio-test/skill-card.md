## Description: <br>
Run a minimal test matrix for the Model Studio skills that exist in this repo, including image/video/audio, realtime speech, omni, visual reasoning, embedding, rerank, and edit variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run one small Alibaba Cloud Model Studio request per supported capability and record model, request, response, duration, and status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can call Alibaba Cloud Model Studio APIs and may trigger billable generation, editing, voice-cloning, or media-processing operations. <br>
Mitigation: Confirm each operation before running it, keep the request scope minimal, and use a dedicated test API key where possible. <br>
Risk: Prompts, media, API responses, and generated artifacts may be saved locally as test evidence. <br>
Mitigation: Avoid sensitive prompts or media, and review or delete saved output files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-entry-modelstudio-test) <br>
- [Source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with inline shell commands and a results table template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local evidence files and result summaries under output/alicloud-ai-entry-modelstudio-test/.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

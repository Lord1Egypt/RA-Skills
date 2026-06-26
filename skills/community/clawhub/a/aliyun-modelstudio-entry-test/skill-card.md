## Description: <br>
Use when running a minimal test matrix for the Model Studio skills that exist in this repo, including image/video/audio, realtime speech, omni, visual reasoning, embedding, rerank, and edit variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a minimal validation matrix across Alibaba Model Studio skills and record model, request, response, duration, and status evidence for each capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make external Alibaba Model Studio API calls using a configured DASHSCOPE_API_KEY. <br>
Mitigation: Use a limited-purpose API key, keep secrets out of prompts and output files, and run only the intended bounded test calls. <br>
Risk: Saved test evidence may include prompt, media, or response details that should not be shared broadly. <br>
Mitigation: Use sanitized sample inputs and review local output files before sharing or publishing them. <br>
Risk: Unpinned SDK installation may change behavior over time. <br>
Mitigation: Pin the dashscope SDK version in controlled environments when reproducibility is required. <br>


## Reference(s): <br>
- [Source list](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-modelstudio-entry-test) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and a results table template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local evidence files and API response summaries under output/aliyun-modelstudio-entry-test/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

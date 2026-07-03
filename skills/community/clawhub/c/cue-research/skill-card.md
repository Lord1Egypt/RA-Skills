## Description: <br>
Cue Research lets an agent run Cue research questions against saved buddy templates or free-form deep research, limited to public-data scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to delegate public-data research questions to Cue, choose between matched saved buddy templates and free-form deep research, and save useful free-form runs for future reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional mimic-file path can upload local documents to Cue's backend. <br>
Mitigation: Do not use mimic-file with confidential, internal, personal, medical, financial, or client documents unless upload is intended. <br>
Risk: The skill depends on Cue API access, local report files under ~/cue-reports, and a sibling cue-buddy installation. <br>
Mitigation: Install only when those dependencies and local output behavior are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [Cue Research skill page](https://clawhub.ai/wangxiaoxu/skills/cue-research) <br>
- [Cue API endpoint](https://cuecue.cn/api) <br>
- [Cue API key page](https://cuecue.cn/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research reports, concise prompts, and shell commands for background runs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under ~/cue-reports; runs require cue-buddy as a sibling skill and may use CUE_API_KEY or CUE_API_BASE.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

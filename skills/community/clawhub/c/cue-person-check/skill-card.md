## Description: <br>
Cue Person Check helps agents run Cue deep research for person background checks, cross-referencing public data and returning source-linked findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent select and run Cue person-check research templates for public-data due diligence, executive history review, related-entity checks, and management risk screening. It is not a substitute for legal, underwriting, or formal diligence review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can handle sensitive person and related-entity due-diligence topics. <br>
Mitigation: Confirm the exact subject and research purpose before running, use only public-data outputs as supporting research, and route legal, underwriting, or formal diligence conclusions to qualified reviewers. <br>
Risk: Running Cue deep research consumes Cue credits. <br>
Mitigation: Ask for explicit user confirmation before each run and state which Cue template and subject will be used. <br>
Risk: The skill asks the agent to clone or update and execute an external Cue runner. <br>
Mitigation: Review the runner source before deployment, keep the Cue API key private, and avoid exposing local Cue configuration in logs or responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangxiaoxu/skills/cue-person-check) <br>
- [Cue Playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue Skills Runner Source](https://github.com/sensedeal/cue-skills) <br>
- [Cue Skills Runner Mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with source links, plus inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent should preserve source links, request credit confirmation before running Cue research, and report empty results without fabrication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

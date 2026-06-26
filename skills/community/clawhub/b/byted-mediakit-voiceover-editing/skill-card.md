## Description: <br>
A Volcano Engine AI MediaKit skill for turning talking-head video or audio inputs into ASR transcripts, editing decisions, review data, and video export artifacts across local, cloud, or SkillHub gateway execution modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media operators, and agent workflows use this skill to process talking-head media, generate ASR-based edit decisions, review proposed cuts, and export edited video through local tooling or Volcano Engine VOD. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review server can expose local files while it is running. <br>
Mitigation: Run the review server only on localhost, stop it after review, and avoid browsing untrusted pages while the server is active. <br>
Risk: Cloud or SkillHub gateway execution can upload media and produce real playback URLs. <br>
Mitigation: Use least-privilege VOD and ASR credentials, test with an isolated media space, and confirm whether generated playback URLs should be shared. <br>
Risk: The security summary says the skill can silently change cloud media publication state. <br>
Mitigation: Review export settings and publication effects before using production media or production VOD spaces. <br>
Risk: Local execution may download or install dependencies and model assets unless they are already provisioned. <br>
Mitigation: Install in an isolated environment and pre-review dependency and model downloads before running local mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volc-ai-mediakit/byted-mediakit-voiceover-editing) <br>
- [Publisher profile](https://clawhub.ai/user/volc-ai-mediakit) <br>
- [Environment configuration template](templates/env.md) <br>
- [EDL editing decision format](references/%E5%86%85%E7%BD%AE/EDL%E7%BC%96%E8%BE%91%E5%86%B3%E7%AD%96%E6%A0%BC%E5%BC%8F.md) <br>
- [ASR semantic correction reference](references/%E5%86%85%E7%BD%AE/ASR%E8%AF%AD%E4%B9%89%E7%BA%A0%E9%94%99.md) <br>
- [Target platform configuration](references/%E5%86%85%E7%BD%AE/%E7%9B%AE%E6%A0%87%E5%B9%B3%E5%8F%B0%E9%85%8D%E7%BD%AE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, json, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, JSON edit/export artifacts, and review/export workflow outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ASR and edit-decision JSON under the task output directory, review page data, export request data, and either local video output paths or VOD OutputVid and PlayURL values depending on execution mode.] <br>

## Skill Version(s): <br>
1.0.9 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

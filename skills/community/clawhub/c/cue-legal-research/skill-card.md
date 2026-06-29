## Description: <br>
Run Cue deep research for legal and industry research scenarios, using multiple public sources to produce source-linked conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Cue-backed legal and industry research across public sources for regulatory research, due diligence, sanctions exposure checks, litigation case review, domestic regulation lookup, and comparative law analysis. The skill guides setup, live template selection, credit confirmation, execution, and source-preserving report delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external Cue runner cloned into the user's home directory. <br>
Mitigation: Install only after reviewing the runner source and keeping the dependency up to date from the documented repository or mirror. <br>
Risk: The Cue runner may read the user's Cue API key from local configuration. <br>
Mitigation: Use a dedicated Cue account or scoped credentials where possible and avoid running the workflow on systems where that access is inappropriate. <br>
Risk: Deep research runs consume Cue credits. <br>
Mitigation: Require explicit user confirmation of the selected template, subject, and credit consumption before each run. <br>
Risk: Research output may be incomplete, unavailable, or unsuitable as legal advice. <br>
Mitigation: Preserve source links, report empty results honestly, and require qualified review before relying on the output for legal, diligence, or compliance decisions. <br>


## Reference(s): <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [cue-skills GitHub repository](https://github.com/sensedeal/cue-skills) <br>
- [cue-skills Gitee mirror](https://gitee.com/sensedeal/cue-skills) <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-legal-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and source-linked research reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch a long-running Cue research job, consume credits after confirmation, and return empty results when no report is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

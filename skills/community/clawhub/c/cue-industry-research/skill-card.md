## Description: <br>
Runs Cue deep research for industry-research scenarios, cross-checking public data sources and returning conclusions with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and research agents use this skill to select a Cue industry-research partner, confirm credit use, run public-data research on sectors, value chains, financial performance, macro policy, or event calendars, and return a sourced report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research requests may send business information to Cue for external processing. <br>
Mitigation: Avoid sending sensitive business information unless the user intends it to be processed by Cue. <br>
Risk: Deep research runs consume Cue credits. <br>
Mitigation: Confirm the selected research partner, subject, and credit use with the user before running. <br>
Risk: The workflow depends on an external Cue runner that may be installed or updated separately. <br>
Mitigation: Review the cue-skills runner source before first use and use a trusted local installation. <br>
Risk: Reports rely on public data and may not satisfy diligence, legal, or underwriting needs on their own. <br>
Mitigation: Treat results as research support and validate important conclusions against authoritative sources. <br>


## Reference(s): <br>
- [Cue Playbook](https://cuecue.cn/playbook) <br>
- [Cue Playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue Skills Runner](https://github.com/sensedeal/cue-skills) <br>
- [Cue Skills Runner Gitee Mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and sourced report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Cue APIs and a local Cue runner; final reports should preserve source links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

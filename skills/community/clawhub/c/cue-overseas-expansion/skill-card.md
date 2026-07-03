## Description: <br>
Run Cue deep research for the Overseas Expansion Leads scenario, cross-referencing public sources and returning conclusions with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business teams use this skill to run Cue-based research for overseas expansion leads, sanctions screening, export-control checks, regulatory disclosure review, and related due diligence. It helps produce source-linked research reports from public data, while requiring user confirmation before credit-consuming runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch or update live runner code under ~/.cue and run it with access to the user's Cue account key. <br>
Mitigation: Review the runner repository before first use, prefer a pinned and reviewed runner version, and avoid installing if this local account access is not acceptable. <br>
Risk: Deep research runs can consume Cue account credits. <br>
Mitigation: Require explicit user confirmation before each credit-spending run and clearly identify the selected research module and subject. <br>
Risk: Research results cover public data and may be incomplete or unsuitable as a substitute for legal, insurance, or formal due-diligence review. <br>
Mitigation: Keep source links attached, do not fabricate missing results, and route high-stakes decisions through qualified review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-overseas-expansion) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue runner repository](https://github.com/sensedeal/cue-skills) <br>
- [Cue runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and source-linked research report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate Cue research runs that consume account credits after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

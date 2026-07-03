## Description: <br>
Runs Cue deep research for margin trading scenarios using cross-source public data and returns conclusions with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to run Cue research for margin-trading questions, including broker policy comparisons, ETF and technology security financing comparisons, and risk-contraction alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch or update unpinned remote runner code under ~/.cue that may run with access to local Cue account credentials. <br>
Mitigation: Review the runner source before installation, prefer a trusted pinned runner version, and confirm what will be installed or updated before first use. <br>
Risk: Running deep research consumes Cue credits. <br>
Mitigation: Ask the user for explicit confirmation before starting any research run that consumes credits. <br>
Risk: Research is based on public data and is not a substitute for due diligence, legal review, or underwriting. <br>
Mitigation: Present results as research support, preserve source links, and avoid treating outputs as final professional advice. <br>
Risk: The live Cue scene or runner may return no content. <br>
Mitigation: Report unavailable or empty results clearly and offer retry options instead of inventing findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-margin-trading) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [cue-skills runner repository](https://github.com/sensedeal/cue-skills) <br>
- [cue-skills runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and final research reports with source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit credit confirmation before running; final reports preserve source links and should not fabricate missing results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and auto changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

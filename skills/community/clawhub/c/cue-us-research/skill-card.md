## Description: <br>
Runs Cue deep research for US equity research by cross-checking public sources and returning sourced conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research users use this skill to run Cue-based US market and company research workflows, including company diagnostics, macro tracking, liquidity reports, COT analysis, industry mapping, and SEC filing monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance and trading output can be mistaken for professional financial advice or an instruction to trade. <br>
Mitigation: Treat generated output as research only, review cited sources, and require user judgment before any financial decision. <br>
Risk: Deep research runs consume Cue credits. <br>
Mitigation: Ask for explicit user confirmation before running a credit-consuming workflow. <br>
Risk: The workflow can clone or update an external Cue runner and call live Cue services. <br>
Mitigation: Use the documented runner sources, review commands before execution, and ensure the user expects external network and account/API-key use. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/wangxiaoxu/skills/cue-us-research) <br>
- [Cue playbook API](https://cuecue.cn/api/playbook) <br>
- [Cue skills runner repository](https://github.com/sensedeal/cue-skills) <br>
- [Cue skills runner mirror](https://gitee.com/sensedeal/cue-skills) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with sourced research reports and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cue account/API key and explicit user confirmation before credit-consuming research runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Use this skill when a user needs financial analysis, earnings research, or investment-related reports generated through the AnyGen CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to route financial research requests to AnyGen for earnings summaries, equity research, financial statement analysis, due diligence, valuation, portfolio, IPO, M&A, and credit analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial inputs may be sent to AnyGen for server-side processing. <br>
Mitigation: Use a dedicated, revocable AnyGen API key and avoid confidential or regulated financial material unless AnyGen's terms are acceptable. <br>
Risk: The skill can direct the agent to install or run the anygen-workflow-generate skill. <br>
Mitigation: Manually inspect and approve that workflow skill before allowing installation or execution. <br>
Risk: The security scan verdict is suspicious. <br>
Mitigation: Review the security guidance before installing and keep human approval in the loop for authentication, installation, and generated financial report use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logictortoise/anygen-financial-research) <br>
- [Publisher profile](https://clawhub.ai/user/logictortoise) <br>
- [AnyGen service](https://www.anygen.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated financial research report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the anygen CLI and ANYGEN_API_KEY; report generation is performed server-side by AnyGen.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

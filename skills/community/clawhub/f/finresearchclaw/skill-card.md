## Description: <br>
Finance, accounting, and investment research automation via the FinResearchClaw repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance researchers use this skill to route event studies, factor-model research, accounting regressions, forecast-error analysis, valuation research, and investment research workflows through the FinResearchClaw repo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clone and run an external finance research repository, including auto-approved workflows. <br>
Mitigation: Review the external repo and selected configs before execution, consider pinning a known commit, and run in a sandbox or dedicated workspace. <br>
Risk: Finance research workflows may use sensitive datasets or costly provider-backed agents. <br>
Mitigation: Use only approved Codex, Claude, or API providers for confidential data and confirm provider costs before long-running analyses. <br>


## Reference(s): <br>
- [FinResearchClaw examples](references/examples.md) <br>
- [FinResearchClaw GitHub repository](https://github.com/ChipmunkRPA/FinResearchClaw) <br>
- [ClawHub skill page](https://clawhub.ai/ChipmunkRPA/finresearchclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May clone or update and run the external FinResearchClaw repo when the user chooses an execution path.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

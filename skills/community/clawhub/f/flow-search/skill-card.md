## Description: <br>
Deep web research using Claude's native search tool for comprehensive research, market analysis, competitor intelligence, and cases where standard search is not enough. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent builders use FlowSearch to run Claude-backed web searches that synthesize multiple sources into direct answers or structured research reports. It is suited for market analysis, competitor intelligence, recent-news context, and other research tasks that benefit from deeper source synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Claude non-interactively while inheriting the shell environment, including Claude authentication. <br>
Mitigation: Run it in a restricted environment with only required environment variables and no sensitive working-directory files. <br>
Risk: The skill disables Claude permission prompts in normal non-root execution. <br>
Mitigation: Review the source before use and remove the permission-bypass flag when interactive permission checks are required. <br>


## Reference(s): <br>
- [FlowSearch ClawHub listing](https://clawhub.ai/windseeker1111/flow-search) <br>
- [Claude Code CLI](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown research report or direct text answer with cited source URLs; TypeScript helpers return structured result objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick searches use a 2 minute timeout; deep research uses a 3 minute timeout.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

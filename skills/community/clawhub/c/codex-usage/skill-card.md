## Description: <br>
Manual Telegram slash-style command for Codex profile status and usage checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeadlySilent](https://clawhub.ai/user/DeadlySilent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Codex users use this skill to handle /codex_usage requests and check profile status, usage limits, and authentication health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper delegates execution to an external local codex-profiler skill and script. <br>
Mitigation: Review and trust the referenced codex-profiler skill and codex_usage.py script before installing or running this wrapper. <br>
Risk: The usage check may inspect all configured Codex profiles and expose profile or authentication-health information. <br>
Mitigation: Run it only in contexts where profile status and auth-health details are appropriate to disclose. <br>


## Reference(s): <br>
- [Codex Usage ClawHub release](https://clawhub.ai/DeadlySilent/codex-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash command and text output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates execution to the local codex-profiler skill script.] <br>

## Skill Version(s): <br>
1.0.19 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

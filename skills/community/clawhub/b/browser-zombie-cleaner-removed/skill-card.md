## Description: <br>
Detects orphaned OpenClaw browser processes left after gateway restarts and can optionally terminate verified matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw browser process buildup, report orphaned browser memory use, and optionally clean verified zombie processes during local maintenance or health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using --kill sends termination signals to matching browser process groups. <br>
Mitigation: Run detection first, review the reported PIDs, avoid broad custom --pattern values, and use conservative --min-age settings before automated cleanup. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default mode is detect-only; process termination requires the explicit --kill option.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

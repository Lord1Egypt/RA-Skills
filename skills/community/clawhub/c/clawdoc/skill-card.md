## Description: <br>
Diagnoses OpenClaw agent failures, cost spikes, performance issues, and recurring session patterns with deterministic shell-based detectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashishjaingithub](https://clawhub.ai/user/ashishjaingithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Clawdoc to inspect OpenClaw session logs, identify failure or cost patterns, and produce concise diagnoses and prescriptions for improving agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect private local agent session logs more broadly than expected. <br>
Mitigation: Use explicit /clawdoc commands with intended paths, review diagnostic output before sharing it, and install only when local session-log analysis is acceptable. <br>
Risk: Enabling CLAWDOC_LEARNINGS can write findings into repository files. <br>
Mitigation: Leave CLAWDOC_LEARNINGS unset unless repository file changes are intended and reviewed. <br>
Risk: Development conversion scripts can affect output directories. <br>
Mitigation: Do not run dev conversion scripts on important output directories. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ashishjaingithub/clawdoc) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [Demo output](docs/demo-output.md) <br>
- [OpenClaw test guide](docs/test-on-openclaw.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize local session logs, costs, token counts, tool calls, detected patterns, and recommended fixes.] <br>

## Skill Version(s): <br>
0.12.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

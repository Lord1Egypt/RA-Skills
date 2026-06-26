## Description: <br>
Generate a playful or sharp daily roast of recent Strava activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ranasalalali](https://clawhub.ai/user/ranasalalali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch recent Strava activity and produce concise, humorous daily workout recaps with configurable tone and intensity. It supports deterministic summaries, JSON context and prompt generation, and a fallback roast path when runtime model generation is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Strava OAuth credentials and can process private workout names, metrics, and recent activity history. <br>
Mitigation: Use it only in trusted workspaces, keep Strava app credentials and token files private, and avoid exposing generated prompts, context JSON, or roast state where workout details are sensitive. <br>
Risk: The security evidence reports an under-scoped reauthorization path that may execute a local Python helper script from a configurable workspace path. <br>
Mitigation: Review and control the reauthorization helper path before use, and only allow helper scripts that are owned and trusted in the local OpenClaw workspace. <br>
Risk: Runtime model generation could invent workout stats or produce unsuitable roast wording if used without checks. <br>
Mitigation: Build deterministic context first, sanity-check generated paragraphs for factual grounding and style, and fall back to the deterministic roast output when generation is unavailable or weak. <br>


## Reference(s): <br>
- [Daily Strava Roast design notes](references/design.md) <br>
- [Daily Strava Roast V2](docs/V2.md) <br>
- [Daily Strava Roast ClawHub page](https://clawhub.ai/ranasalalali/daily-strava-roast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus CLI text or JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Roasts are intended to be short, fact-grounded paragraphs; context and summary modes can emit machine-readable JSON.] <br>

## Skill Version(s): <br>
0.2.5 (source: pyproject.toml, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

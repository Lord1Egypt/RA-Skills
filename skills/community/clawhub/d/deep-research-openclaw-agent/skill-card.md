## Description: <br>
Install and wire a structured OpenClaw deep-research sub-agent with hybrid search, artifact-based runs, claim verification, report linting, and validated finalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MilleniumGenAI](https://clawhub.ai/user/MilleniumGenAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure a reproducible deep-research sub-agent workflow with planning, source collection, claim verification, report linting, and finalization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to clone and run code from an external GitHub repository. <br>
Mitigation: Review or pin the referenced repository, inspect copied prompt files and Python scripts, and avoid elevated privileges before using it. <br>
Risk: Research prompts and external search providers may handle user-provided topics or source material. <br>
Mitigation: Use a limited Tavily key when enabling Tavily-backed scouting and avoid submitting secrets or sensitive private material unless the configured agent and providers are approved for that data. <br>


## Reference(s): <br>
- [Repository homepage](https://github.com/MilleniumGenAI/deep-research-openclaw-agent) <br>
- [Root README](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/README.md) <br>
- [Sub-agent contract](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/workspace-researcher/SOUL.md) <br>
- [Main handoff contract](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/main-deep-research-skill.md) <br>
- [Runtime scripts](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/tree/main/openclaw/workspace-researcher/scripts) <br>
- [Agent config template](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/agent-config.template.json) <br>
- [Known limits](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/docs/known-limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce validation commands and OpenClaw agent invocation examples; Tavily-backed scouting requires a configured Tavily key.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

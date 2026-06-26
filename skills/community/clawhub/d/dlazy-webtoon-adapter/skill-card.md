## Description: <br>
Adapts web novels into Chinese webtoon or comic scripts through genre selection, plot breakdown, episode tagging, per-episode script writing, and quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, comic production teams, and agents use this skill to convert user-provided web-novel chapters or revision notes into structured Chinese webtoon breakdowns and episode scripts. It can also guide confirmed, single-step dLazy CLI generation commands when visual outputs are requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be saved in local CLI configuration. <br>
Mitigation: Use an environment variable or npx flow when avoiding persistent global configuration, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Prompts and media may be sent to dLazy API and file services. <br>
Mitigation: Review inputs before sending them, avoid sensitive material unless the user accepts that transfer, and make cloud API use clear before generation. <br>
Risk: The skill can lead an agent to run local dLazy CLI generation commands. <br>
Mitigation: Review each command before allowing execution and run only explicit, single generation commands after user confirmation. <br>


## Reference(s): <br>
- [Dlazy Webtoon Adapter on ClawHub](https://clawhub.ai/dlazyai/dlazy-webtoon-adapter) <br>
- [dLazy CLI source and homepage](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy website](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown conversation output with structured Chinese adaptation sections and inline shell commands when generation is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on the conversation context and may include prompts, episode breakdowns, scripts, revision guidance, and explicit dLazy CLI commands for user-approved generation steps.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

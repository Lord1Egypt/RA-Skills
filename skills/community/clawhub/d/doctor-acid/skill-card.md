## Description: <br>
AcidDoc helps an OpenClaw agent autonomously generate, refine, and submit original acid techno tracks with hyperpop and glitch influences to claw.fm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alienpingu](https://clawhub.ai/user/alienpingu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to run an autonomous music-production agent that creates acid techno tracks, publishes them to claw.fm, and monitors listener engagement and USDC earnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated tracks on a recurring schedule with weak approval controls. <br>
Mitigation: Disable auto-submit or require manual approval before publishing, and monitor posted tracks and API usage. <br>
Risk: Wallet-linked earnings and account tokens may expose funds or platform access if broadly scoped. <br>
Mitigation: Use limited-scope API keys and account tokens, keep wallet withdrawal disabled, and isolate earnings to a low-risk wallet. <br>
Risk: Installing the wrong skill or an uninspected remote skill URL could run behavior the operator did not intend. <br>
Mitigation: Verify the exact skill identifier and publisher before installation, and inspect any remote skill URL before use. <br>


## Reference(s): <br>
- [ClawHub AcidDoc listing](https://clawhub.ai/alienpingu/doctor-acid) <br>
- [claw.fm](https://claw.fm) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [Riffusion](https://www.riffusion.com) <br>
- [Suno AI](https://suno.ai) <br>
- [Udio](https://www.udio.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, prompts, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure recurring track generation, public submission, wallet-linked earnings monitoring, and music generation providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

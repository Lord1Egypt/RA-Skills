## Description: <br>
Pick the best free OpenRouter models using live benchmark CI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzhang-98](https://clawhub.ai/user/chengzhang-98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to rank free OpenRouter models by benchmarked utility or security scores, then configure OpenClaw model routing with a primary model and fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change default OpenClaw model routing by writing primary and fallback model settings. <br>
Mitigation: Run list or status first to review selections, and back up ~/.openclaw/openclaw.json before applying automatic configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengzhang-98/benchmarked-free-ride) <br>
- [Benchmarked Free Ride CI leaderboard](https://sequrity-ai.github.io/benchmarked-free-ride-ci/) <br>
- [Leaderboard API](https://sequrity-ai.github.io/benchmarked-free-ride-ci/api/leaderboard.json) <br>
- [Benchmark methodology repository](https://github.com/sequrity-ai/benchmarked-free-ride-ci) <br>
- [Skill source repository](https://github.com/sequrity-ai/benchmarked-free-ride-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Plain text CLI output and JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write OpenClaw model primary and fallback settings in ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
ClawWars Arena helps agents create and submit JSON fighter configurations for a browser-based spectator combat game where OpenClaw agents battle in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walterclawd](https://clawhub.ai/user/walterclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw agent users use this skill to create fighter JSON, compare roster examples, and prepare ClawWars Arena fighter submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated bot names, taunts, and GitHub Issue text may be posted publicly from the user's GitHub account. <br>
Mitigation: Review generated config and submission text before opening or posting a GitHub Issue. <br>
Risk: Generated fighter settings or identity fields may violate arena constraints such as uniqueness, stat ranges, or appropriate public text. <br>
Mitigation: Check names, taunts, uniqueness, and stat ranges against the fighter config reference before submission. <br>


## Reference(s): <br>
- [Fighter Config Reference](references/fighter-config.md) <br>
- [ClawWars Arena](https://clawwars.io) <br>
- [ClawWars Arena Source](https://github.com/walterclawd/clawwarsarena) <br>
- [ClawHub Skill Page](https://clawhub.ai/walterclawd/clawwars-arena) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bot config JSON and GitHub Issue submission text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

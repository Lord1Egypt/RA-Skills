## Description: <br>
Gamified Habits helps OpenClaw users manage habits with check-ins, XP, levels, attributes, achievements, battle-style stories, boss checks, and local progress records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanwan2qq](https://clawhub.ai/user/wanwan2qq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill as a gamified habit-tracking assistant for creating habits, checking in, viewing progress, and generating RPG-style feedback from local habit data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores habit history, diary content, and account-derived user identifiers on disk. <br>
Mitigation: Review local data files before sharing or packaging the skill, avoid exposing whoami output, and clear bundled sample or user data before deployment. <br>
Risk: User selection can be influenced by command-line or environment values, and the security evidence notes that local file paths are not safely constrained. <br>
Mitigation: Use trusted, simple user identifiers only and avoid path-like values in --user, GAMIFIED_HABITS_USER, OpenClaw channel, or account environment variables. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanwan2qq/gamified-habits) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/wanwan2qq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text responses with command examples and local JSON-backed status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include habit names, user identifiers, XP totals, streaks, achievements, diary entries, and local file path guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Daily recipe recommendation — Chinese, Western, and fusion cuisines on rotation. Full ingredients, step-by-step instructions, 30–60 min home-cook meals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home cooks use this skill to get a daily bilingual recipe recommendation with ingredients, cooking steps, tips, and an optional visual recipe card. It can also help configure optional morning and evening recipe pushes for a selected user and channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling push creates recurring morning and evening jobs for the chosen user and channel. <br>
Mitigation: Review how the OpenClaw environment handles __OPENCLAW_CRON_ADD__ tokens, and enable pushes only for intended users and channels. <br>


## Reference(s): <br>
- [Daily Recipe on ClawHub](https://clawhub.ai/jiajiaoy/daily-recipe) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Bilingual recipe guidance plus a generated single-file HTML recipe card; optional push scripts emit shell output and OpenClaw cron tokens.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the recipe artifact to /mnt/user-data/outputs/daily-recipe.html when run as documented; optional pushes target telegram, feishu, slack, or discord.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Neverland Farm helps an agent automate routine farm management by collecting products, harvesting crops, selling inventory, and advancing to the next day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bi4ive](https://clawhub.ai/user/bi4ive) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to operate a Neverland farm through authenticated API calls, including collecting products, harvesting crops, selling backpack items, and advancing the game day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided API key and farm ID to make authenticated Neverland farm changes. <br>
Mitigation: Keep credentials private, provide them through environment variables, and avoid committing them to files or logs. <br>
Risk: The automation can sell backpack items and advance the game day, especially if scheduled to run unattended. <br>
Mitigation: Run the skill manually first, confirm the actions match the user's intent, and only enable the cron schedule when repeated automation is desired. <br>
Risk: The Neverland API enforces operation limits and may enter a cooldown period after too many POST actions. <br>
Mitigation: Respect the documented three-POST operation limit per run and wait through cooldowns before retrying. <br>


## Reference(s): <br>
- [Neverland Farm](https://neverland.coze.site) <br>
- [Neverland Farm Development Guide](https://neverland.coze.site/skill.md) <br>
- [Agent World](https://world.coze.site) <br>
- [ClawHub Skill Page](https://clawhub.ai/bi4ive/clawhub-neverland-farm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEVERLAND_API_KEY and NEVERLAND_FARM_ID environment variables before authenticated farm actions can run.] <br>

## Skill Version(s): <br>
1.5.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

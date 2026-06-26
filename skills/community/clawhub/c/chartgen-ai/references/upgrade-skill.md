# Skill Upgrade Procedure

When the tool returns `"error": "upgrade_required"`, the tool version is outdated.
The response includes `current_version` and `min_version`.

Tell the user to update manually (adapt to their language):

> ⚠️ ChartGen skill version **{current_version}** is outdated (requires **{min_version}**).
> Please update the skill:
> - **ClawHub**: search "chartgen" and reinstall
> - **GitHub**: `git -C <skill_dir> pull` or reinstall from
>   `https://github.com/chartgen-ai/chartgen-skill`

**Stop here** — do not retry or continue the task.
